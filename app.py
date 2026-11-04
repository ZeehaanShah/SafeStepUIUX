"""SafeStep — stay one step ahead of scams.  Streamlit app (English / हिंदी / मराठी).

Run locally:   streamlit run app.py
Deploy:        push this folder to GitHub → share.streamlit.io → New app → app.py
Live OTP + AI: add keys in .streamlit/secrets.toml (or the app's Secrets box on Streamlit Cloud).
"""
import copy
import html
import json
import random
import re
import time
from datetime import date
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

from safestep import assistant, otp
from safestep.checker import analyze, highlight
from safestep.content import (ALL_BADGES, ELEC, EXAMPLES, FACTS, FALLBACK_FACT, QOK, QTYPES, SCEN, SCEN_TERM, TERM, TERMS, TIPS)
from safestep.i18n import L, LANGS, lang, t
from safestep.icons import ic
from safestep.styles import inject

st.set_page_config(page_title="SafeStep — stay one step ahead of scams", page_icon="assets/icon.png", layout="wide",
                   initial_sidebar_state="auto")
esc = html.escape


def md(*args):
    """Render an HTML block into the page (st.markdown keeps it in the main DOM so the global CSS applies)."""
    where, body = (st, args[0]) if len(args) == 1 else args
    body = "\n".join(line for line in str(body).splitlines() if line.strip())  # blank lines would end the HTML block
    where.markdown(body, unsafe_allow_html=True)

# ------------------------------------------------------------------ state
SEED = dict(
    lang="en", size=1, authed=False, page="home", scen_idx=0, phone="", ph4="3210",
    viewed=["Phishing", "Smishing", "OTP Fraud", "QR Code Scam"], last_viewed="QR Code Scam", quiz={},
    scen={"The Bank Call": {"first": True}, "The Delivery Message": {"first": False}, "The Shop QR Code": {"first": True}},
    badges=["Calm Caller", "QR Guard", "Caller ID Champion"], checks=5, shared=False,
    toggles=dict(recap=True, tip=True, alerts=False), days=[1, 2, 4], tip_i=0, help_done=[], pf="all", lf="all",
    ask_res=None, chat=[], chat_times=[], otp_stage="phone", otp_sent_at=0.0, otp_err="", dev_code=None,
    confirm_reset=False, alert_gone=False, pick={}, reveal=False, term_open=None, qz=None, celebrate=False, flash=None, goto=None,
)
for k, v in SEED.items():
    st.session_state.setdefault(k, copy.deepcopy(v))
S = st.session_state
inject([0.94, 1.0, 1.12][S.size], lang() != "en")

NAV = [("home", ":material/home:", ["Home", "होम", "होम"]),
       ("ask", ":material/search:", ["Ask Before You Click", "क्लिक करने से पहले पूछें", "क्लिक करण्यापूर्वी विचारा"]),
       ("learn", ":material/menu_book:", ["Learn a Word", "एक शब्द सीखें", "एक शब्द शिका"]),
       ("practice", ":material/verified_user:", ["Practice a Scenario", "अभ्यास करें", "सराव करा"]),
       ("games", ":material/sports_esports:", ["Mini Games", "मिनी गेम्स", "मिनी गेम्स"]),
       ("recap", ":material/event_available:", ["My Weekly Recap", "मेरा साप्ताहिक सारांश", "माझा साप्ताहिक सारांश"]),
       ("assistant", ":material/forum:", ["SafeStep Assistant", "SafeStep सहायक", "SafeStep सहाय्यक"]),
       ("account", ":material/person:", ["My Account", "मेरा खाता", "माझे खाते"])]


# ------------------------------------------------------------------ small helpers
def go(page: str, **extra):
    S.goto = page
    S.pick, S.reveal, S.confirm_reset, S.term_open, S.qz = {}, False, False, None, None
    for k, v in extra.items():
        S[k] = v


def flash(msg: str, icon: str = "✅"):
    S.flash = (msg, icon)


def open_term(key: str):
    S.term_open = key
    S.qz = {"term": key, "step": 1, "picks": {}}
    if key not in S.viewed:
        S.viewed.append(key)
    S.last_viewed = key


def safe_count() -> int:
    seeded = {"The Bank Call", "The Delivery Message", "The Shop QR Code"}
    return 3 + sum(1 for q in S.quiz.values() if q.get("done")) + sum(1 for k, v in S.scen.items() if k not in seeded and v["first"])


def today_idx() -> int:
    return date.today().weekday()


def day_labels():
    return ["सो", "मं", "बु", "गु", "शु", "श", "र"] if lang() != "en" else ["M", "T", "W", "T", "F", "S", "S"]


def mask_phone() -> str:
    return "+91 ••••• •" + str(S.ph4)[-4:]


def header(title: str, sub: str = "", show_help: bool = True):
    c1, c2 = st.columns([5, 1.6], vertical_alignment="center")
    md(c1, f'<div class="ss-title"><h1>{esc(title)}</h1>{f"<p>{esc(sub)}</p>" if sub else ""}</div>')
    if show_help:
        c2.button(t("Need Help Now?", "अभी मदद चाहिए?", "आत्ता मदत हवी आहे?"), key="helpbtn", icon=":material/support:",
                  on_click=go, args=("help",), use_container_width=True)


def meter(pos: float) -> str:
    return (f'<div class="meter"><div class="track"><span class="knob" style="--pos:{pos * 100:.0f}%"></span></div>'
            f'<div class="ends"><span>{t("Safe", "सुरक्षित", "सुरक्षित")}</span><span>{t("Risky", "जोखिम भरा", "धोकादायक")}</span></div></div>')


def lang_switch(where: str):
    def _set():
        val = S.get(f"lang_{where}")
        if val:
            S.lang = val
            flash({"en": "Language changed to English", "hi": "भाषा हिंदी में बदल दी गई", "mr": "भाषा मराठीत बदलली"}[val], "🌐")
    st.segmented_control("Language / भाषा", list(LANGS), format_func=LANGS.get, key=f"lang_{where}", default=lang(),
                         required=True, on_change=_set, label_visibility="collapsed")


OTP_ERR = {
    "invalid_phone": ["Please enter a valid 10-digit Indian mobile number.", "कृपया सही 10 अंकों का भारतीय मोबाइल नंबर डालें।", "कृपया योग्य 10 अंकी भारतीय मोबाइल नंबर टाका."],
    "rate_limited": ["Too many tries. Please wait a few minutes and try again.", "बहुत ज़्यादा कोशिशें हो गईं। कुछ मिनट रुककर फिर कोशिश करें।", "खूप जास्त प्रयत्न झाले. काही मिनिटे थांबून पुन्हा प्रयत्न करा."],
    "wrong_code": ["That code didn’t match. Please check the SMS and try again.", "यह कोड मेल नहीं खाया। SMS देखकर फिर कोशिश करें।", "हा कोड जुळला नाही. SMS पाहून पुन्हा प्रयत्न करा."],
    "expired": ["This code has expired. Tap “Resend code” for a new one.", "यह कोड पुराना हो गया है। नया कोड पाने के लिए “कोड दोबारा भेजें” दबाएं।", "हा कोड कालबाह्य झाला आहे. नवीन कोडसाठी “कोड पुन्हा पाठवा” दाबा."],
    "short": ["Please enter all 6 digits.", "कृपया सभी 6 अंक डालें।", "कृपया सर्व 6 अंक टाका."],
    "send_failed": ["We couldn’t send or check the code right now. Please try again.", "अभी कोड भेज या जांच नहीं पाए। कृपया फिर कोशिश करें।", "आत्ता कोड पाठवता किंवा तपासता आला नाही. कृपया पुन्हा प्रयत्न करा."],
}


# ------------------------------------------------------------------ login
def page_login():
    left, right = st.columns([1.05, 1], gap="large")
    md(left, f'''<div class="hero"><div class="brand" style="color:#fff;padding:0">{ic("shield", "1.9em", "#fff")}SafeStep</div>
<h1>{t("Stay one step<br>ahead of scams.", "ठगी से<br>एक कदम आगे रहें।", "फसवणुकीपासून<br>एक पाऊल पुढे राहा.")}</h1>
<p>{t("Short, friendly practice that helps you spot fake calls, messages and links — at your own pace.", "छोटे, आसान अभ्यास जो आपको नकली कॉल, संदेश और लिंक पहचानने में मदद करते हैं — अपनी रफ़्तार से।", "छोटे, सोपे सराव जे तुम्हाला बनावट कॉल, संदेश आणि लिंक ओळखायला मदत करतात — तुमच्या स्वतःच्या गतीने.")}</p>
<ul>{"".join(f"<li>{ic('check')}<span>{x}</span></li>" for x in [t("Built for first-time smartphone users", "पहली बार स्मार्टफोन चलाने वालों के लिए बना", "पहिल्यांदा स्मार्टफोन वापरणाऱ्यांसाठी बनवलेले"), t("Large text and plain words, in English, हिंदी or मराठी", "बड़े अक्षर और आसान शब्द, हिंदी, मराठी या English में", "मोठी अक्षरे आणि सोपे शब्द — मराठी, हिंदी किंवा English मध्ये"), t("No scores, no pressure — just practice", "कोई नंबर नहीं, कोई दबाव नहीं — बस अभ्यास", "गुण नाहीत, दबाव नाही — फक्त सराव")])}</ul>
<div class="demo-sms" aria-hidden="true"><div class="bubble">{t("Dear Customer, your account will be blocked today. Verify now: bit.ly/kyc-now", "प्रिय ग्राहक, आपका खाता आज बंद हो जाएगा। अभी सत्यापित करें: bit.ly/kyc-now", "प्रिय ग्राहक, तुमचे खाते आज बंद होईल. आत्ताच पडताळणी करा: bit.ly/kyc-now")}</div>
<span class="tag">{ic("warn", "1em")}{t("Creates urgency", "जल्दबाज़ी पैदा करता है", "घाई करायला लावतो")}</span><span class="tag">{ic("warn", "1em")}{t("Asks to click a link", "लिंक पर क्लिक करने को कहता है", "लिंकवर क्लिक करायला सांगतो")}</span><span class="tag">{ic("warn", "1em")}{t("Doesn’t use your name", "आपका नाम नहीं लेता", "तुमचे नाव वापरत नाही")}</span><span class="stamp">{t("Scam spotted", "ठगी पकड़ी गई", "फसवणूक ओळखली")}</span></div></div>''')
    with right:
        lang_switch("login")
        with st.container(border=True):
            if S.otp_stage == "phone":
                md(f'<div class="stepbar"><span><i class="on"></i><i></i></span>{t("Step 1 of 2", "चरण 1 / 2", "पायरी 1 / 2")}</div>')
                st.markdown(f"## {t('Welcome to SafeStep', 'SafeStep में आपका स्वागत है', 'SafeStep मध्ये तुमचे स्वागत आहे')}")
                st.markdown(t("Enter your mobile number. We’ll send you a 6-digit code to sign in.", "अपना मोबाइल नंबर डालें। हम साइन इन के लिए आपको 6 अंकों का कोड भेजेंगे।", "तुमचा मोबाइल नंबर टाका. साइन इन करण्यासाठी आम्ही तुम्हाला 6 अंकी कोड पाठवू."))
                with st.form("phone_form", border=False):
                    num = st.text_input(t("Mobile number (+91)", "मोबाइल नंबर (+91)", "मोबाइल नंबर (+91)"), value=S.phone, max_chars=11,
                                        placeholder=t("10-digit mobile number", "10 अंकों का मोबाइल नंबर", "10 अंकी मोबाइल नंबर"))
                    st.caption("🔒 " + t("We’ll never share your number with anyone.", "हम आपका नंबर कभी किसी के साथ साझा नहीं करेंगे।", "आम्ही तुमचा नंबर कधीही कोणाला देणार नाही."))
                    sent = st.form_submit_button(t("Send Code", "कोड भेजें", "कोड पाठवा"), type="primary", use_container_width=True, icon=":material/arrow_forward:")
                if sent:
                    digits = re.sub(r"\D", "", num or "")[-10:]
                    S.phone = digits
                    if not otp.PHONE_RE.match(digits):
                        st.error(L(OTP_ERR["invalid_phone"]))
                    else:
                        with st.spinner(t("Sending code…", "कोड भेजा जा रहा है…", "कोड पाठवत आहोत…")):
                            ok, err, dev = otp.send_code(digits, lang())
                            time.sleep(0.4)
                        if ok:
                            S.otp_stage, S.otp_sent_at, S.dev_code, S.otp_err = "code", time.time(), dev, ""
                            flash(t("Code sent to your phone", "कोड आपके फोन पर भेज दिया गया", "कोड तुमच्या फोनवर पाठवला आहे"), "📩")
                            st.rerun()
                        st.error(L(OTP_ERR.get(err, OTP_ERR["send_failed"])))
            else:
                md(f'<div class="stepbar"><span><i class="on"></i><i class="on"></i></span>{t("Step 2 of 2", "चरण 2 / 2", "पायरी 2 / 2")}</div>')
                st.markdown(f"## {t('Enter your code', 'अपना कोड डालें', 'तुमचा कोड टाका')}")
                st.markdown(t("We sent a 6-digit code to", "हमने 6 अंकों का कोड भेजा है:", "आम्ही 6 अंकी कोड पाठवला आहे:") + f" **+91 {S.phone[:5]} {S.phone[5:]}**")
                p = otp.provider()
                hint = {"demo": t("Demo: type any 6 digits.", "डेमो: कोई भी 6 अंक डालें।", "डेमो: कोणतेही 6 अंक टाका."),
                        "console": t("Developer mode: the code is printed in the app logs.", "डेवलपर मोड: कोड ऐप लॉग में दिखेगा।", "डेव्हलपर मोड: कोड ॲप लॉगमध्ये दिसेल.")}.get(
                    p, t("Check your SMS for the 6-digit code.", "6 अंकों का कोड अपने SMS में देखें।", "6 अंकी कोड तुमच्या SMS मध्ये पाहा."))
                if S.dev_code:
                    st.info(t("Developer mode — your code is", "डेवलपर मोड — आपका कोड है", "डेव्हलपर मोड — तुमचा कोड आहे") + f" **{S.dev_code}**", icon=":material/developer_mode:")
                with st.form("code_form", border=False):
                    code = st.text_input(t("6-digit code", "6 अंकों का कोड", "6 अंकी कोड"), max_chars=6, placeholder="••••••", help=hint)
                    st.caption(hint)
                    verify = st.form_submit_button(t("Verify", "सत्यापित करें", "पडताळणी करा"), type="primary", use_container_width=True)
                if verify:
                    code = re.sub(r"\D", "", code or "")
                    if len(code) < 6:
                        st.error(L(OTP_ERR["short"]))
                    else:
                        with st.spinner(t("Verifying…", "सत्यापित हो रहा है…", "पडताळणी सुरू आहे…")):
                            ok, err = otp.check_code(S.phone, code)
                            time.sleep(0.3)
                        if ok:
                            md(f'<div class="success"><svg viewBox="0 0 52 52" width="80" height="80"><circle cx="26" cy="26" r="24"/><path d="M15 27l7 7 15-15"/></svg><h3>{t("You’re in!", "आप साइन इन हो गए!", "तुम्ही साइन इन झालात!")}</h3></div>')
                            time.sleep(0.9)
                            S.authed, S.ph4, S.otp_stage, S.dev_code, S.page = True, S.phone[-4:], "phone", None, "home"
                            flash(t("Signed in. Welcome back, Meena!", "साइन इन हो गया। स्वागत है, मीना!", "साइन इन झाले. पुन्हा स्वागत आहे, मीना!"), "👋")
                            st.rerun()
                        st.error(L(OTP_ERR.get(err, OTP_ERR["send_failed"])))
                c1, c2 = st.columns(2)
                if c1.button(t("Change number", "नंबर बदलें", "नंबर बदला"), icon=":material/arrow_back:", use_container_width=True):
                    S.otp_stage = "phone"; st.rerun()
                wait = 30 - int(time.time() - S.otp_sent_at)
                if wait > 0:
                    c2.caption(t(f"Didn’t get it? You can resend in 0:{wait:02d}", f"कोड नहीं मिला? 0:{wait:02d} में दोबारा भेज सकते हैं", f"कोड मिळाला नाही? 0:{wait:02d} नंतर पुन्हा पाठवू शकता"))
                elif c2.button(t("Resend code", "कोड दोबारा भेजें", "कोड पुन्हा पाठवा"), icon=":material/refresh:", use_container_width=True):
                    ok, err, dev = otp.send_code(S.phone, lang())
                    if ok:
                        S.otp_sent_at, S.dev_code = time.time(), dev
                        flash(t("A new code is on its way", "नया कोड भेजा जा रहा है", "नवीन कोड पाठवत आहोत"), "📩"); st.rerun()
                    st.error(L(OTP_ERR.get(err, OTP_ERR["send_failed"])))
        st.caption("🛡️ " + t("SafeStep will never ask for your bank PIN or password.", "SafeStep कभी भी आपका बैंक पिन या पासवर्ड नहीं मांगेगा।", "SafeStep कधीही तुमचा बँक पिन किंवा पासवर्ड मागणार नाही."))


# ------------------------------------------------------------------ sidebar
def sidebar():
    with st.sidebar:
        if S.toggles["tip"]:
            md(f'<div class="tipcard"><b>{ic("bulb", "1.1em")}{t("Safety tip", "सुरक्षा टिप", "सुरक्षा टीप")}</b>{esc(L(TIPS[S.tip_i % len(TIPS)]))}</div>')
            st.button(t("Next tip", "अगली टिप", "पुढची टीप"), key="nexttip", icon=":material/arrow_forward:", type="tertiary",
                      on_click=lambda: S.update(tip_i=S.tip_i + 1))
        md(f'<div class="me"><span class="avatar">M</span><span><b>{t("Meena Sharma", "मीना शर्मा", "मीना शर्मा")}</b><small>{mask_phone()}</small></span></div>')


# ------------------------------------------------------------------ word card + quiz (dialog)
def _close_term():
    S.term_open, S.qz = None, None


@st.dialog(" ", width="large", on_dismiss=_close_term)
def term_dialog(key: str):
    x = TERM[key]
    qz = S.qz or {"term": key, "step": 1, "picks": {}}
    S.qz = qz
    md(f'<div class="row" style="flex-wrap:nowrap"><span class="ibox">{ic(x["icon"], "1.8em")}</span><div><span class="eyebrow">{esc(L(x["cat"]))}</span><h2 style="margin:0">{esc(L(x["name"]))}</h2></div></div>')
    info, quiz = st.columns([1, 1.05], gap="large")
    md(info, f'''<span class="lab">{t("What it is", "यह क्या है", "हे काय आहे")}</span><p>{esc(L(x["d"]))}</p>
<span class="lab">{t("Example", "उदाहरण", "उदाहरण")}</span><div class="box ex">{esc(L(x["ex"]))}</div>
<span class="lab">{t("How to stay safe", "सुरक्षित कैसे रहें", "सुरक्षित कसे राहावे")}</span><div class="box tip">{ic("shield")}<span>{esc(L(x["tip"]))}</span></div>
<span class="lab">{t("Remember this", "इसे याद रखें", "हे लक्षात ठेवा")}</span><div class="box rem">{ic("bulb")}<span>{esc(L(x["rem"]))}</span></div>''')
    with quiz:
        step = qz["step"]
        dots = "".join(f'<i class="{"ans" if j in qz["picks"] else ""} {"cur" if j == step else ""}"></i>' for j in range(1, 6))
        prog = 100 if step == "done" else len(qz["picks"]) * 20
        md(f'<div class="row" style="justify-content:space-between"><h3 style="margin:0">{t("Quick Check", "झटपट जांच", "झटपट तपासणी")}</h3><div class="dots">{dots}</div></div><div class="qprog"><i style="width:{prog}%"></i></div>')
        if step == "done":
            if S.celebrate:
                st.balloons(); S.celebrate = False
            if S.flash:
                st.toast(S.flash[0], icon=S.flash[1]); S.flash = None
            md(f'<div class="done"><span class="medal">{ic("check", "2em")}</span><b style="font-size:1.25rem">{t("You’ve got a good sense of this one now", "अब आपको यह शब्द अच्छी तरह समझ आ गया है", "आता हा शब्द तुम्हाला चांगला समजला आहे")}</b><span class="muted">{t("Come back anytime to refresh it.", "याद ताज़ा करने के लिए कभी भी वापस आएं।", "उजळणीसाठी कधीही परत या.")}</span></div>')
            if st.button(t("Back to word list", "शब्दों की सूची पर वापस जाएं", "शब्दांच्या यादीकडे परत जा"), type="primary", use_container_width=True):
                _close_term(); st.rerun()
            st.button(t("Review questions", "सवाल दोबारा देखें", "प्रश्न पुन्हा पाहा"), type="tertiary", on_click=lambda: qz.update(step=1, picks={}))
            return
        row = x["quiz"][step - 1]
        pick = qz["picks"].get(step)
        md(f'<span class="qtype">{esc(L(QTYPES[step - 1]))}</span><p style="font-weight:600;font-size:1.1rem;margin:.2rem 0 .6rem">{esc(L(row["q"]))}</p>')
        for letter, txt in (("A", L(row["a"])), ("B", L(row["b"]))):
            if pick is None:
                def answer(letter=letter):
                    qz["picks"][step] = letter
                    S.quiz.setdefault(key, {"answers": {}})["answers"][str(step)] = letter
                st.button(f"**{letter}** · {txt}", key=f"choice_q{step}{letter}", use_container_width=True, on_click=answer)
            else:
                cls = ("correct" if letter == row["correct"] else "dim") if pick == row["correct"] else ("wrong" if letter == pick else ("safer" if letter == row["correct"] else "dim"))
                mark = ic("check") if cls in ("correct", "safer") else ""
                md(f'<div class="picked {cls}"><span class="L">{letter}</span><span style="flex:1">{esc(txt)}</span>{mark}</div>')
        if pick is not None:
            if pick == row["correct"]:
                md(f'<div class="fb ok">{ic("check")}<span><b>{esc(L(QOK[step - 1]))}</b>{t("You picked the safer choice.", "आपने सुरक्षित विकल्प चुना।", "तुम्ही सुरक्षित पर्याय निवडला.")}</span></div>')
            else:
                md(f'<div class="fb no">{ic("bulb")}<span><b>{t("Let’s look closer.", "आइए ध्यान से देखें।", "चला, नीट पाहूया.")}</b>{esc(L(row["fb"]))}</span></div>')
            last = step == 5

            def advance():
                if last:
                    qz["step"] = "done"
                    S.quiz.setdefault(key, {"answers": {}})["done"] = True
                    if "Word Wise" not in S.badges:
                        S.badges.append("Word Wise")
                        S.flash = (t("New badge: “Word Wise”", "नया बैज: “Word Wise”", "नवीन बॅज: “Word Wise”"), "🏅")
                    S.celebrate = True
                else:
                    qz["step"] = step + 1
            st.button(t("Finish", "पूरा करें", "पूर्ण करा") if last else t("Next question", "अगला सवाल", "पुढचा प्रश्न"), type="primary", icon=":material/arrow_forward:", on_click=advance, key=f"next_{step}")
        else:
            st.caption(t("Not a test — take your time, or close anytime.", "यह परीक्षा नहीं है — आराम से सोचें, या कभी भी बंद करें।", "ही परीक्षा नाही — निवांत विचार करा, किंवा कधीही बंद करा."))


# ------------------------------------------------------------------ pages
def page_home():
    n = safe_count()
    header(t("Hi Meena, stay safe today!", "नमस्ते मीना, आज सुरक्षित रहें!", "नमस्कार मीना, आज सुरक्षित राहा!"),
           t("Your safe space to practise.", "अभ्यास के लिए आपकी सुरक्षित जगह।", "सरावासाठी तुमची सुरक्षित जागा."))
    if S.toggles["alerts"] and not S.alert_gone:
        md(f'<div class="alert"><span class="ibox">{ic("bell")}</span><div><b>{t("New scam alert: fake electricity bill SMS", "नई ठगी अलर्ट: नकली बिजली बिल SMS", "नवीन फसवणूक इशारा: बनावट वीज बिल SMS")}</b><div class="muted">{t("Messages say your power will be cut tonight unless you call a number. Your electricity board never does this.", "संदेश कहते हैं कि किसी नंबर पर कॉल नहीं किया तो आज रात बिजली कट जाएगी। बिजली विभाग ऐसा कभी नहीं करता।", "संदेशात म्हटले जाते की एखाद्या नंबरवर कॉल केला नाही तर आज रात्री वीज कापली जाईल. वीज मंडळ असे कधीच करत नाही.")}</div></div></div>')
        a1, a2, _ = st.columns([1.3, 1, 2])
        a1.button(t("Check a message like this", "ऐसा संदेश जांचें", "असा संदेश तपासा"), icon=":material/search:", on_click=lambda: (go("ask"), S.update(ask_area=L(ELEC), ask_res=None)))
        a2.button(t("Dismiss alert", "अलर्ट हटाएं", "इशारा काढा"), type="tertiary", on_click=lambda: S.update(alert_gone=True))
    days = set(S.days) | {today_idx()}
    off = 263.9 * (1 - min(1, n / 10))
    c1, c2 = st.columns([2, 1], gap="medium")
    md(c1, f'''<div class="streak"><div style="flex:1;min-width:14rem"><h2><span class="ibox amber" style="background:#fff;width:3rem;height:3rem">{ic("shield")}</span>{t(f"{n} Safe Decisions This Week", f"इस हफ्ते {n} सुरक्षित फैसले", f"या आठवड्यात {n} सुरक्षित निर्णय")}</h2>
<span class="muted">{t("Every check, word and scenario counts. Keep going at your own pace.", "हर जांच, हर शब्द और हर अभ्यास गिना जाता है। अपनी रफ़्तार से चलते रहें।", "प्रत्येक तपासणी, शब्द आणि सराव मोजला जातो. तुमच्या गतीने पुढे चालत राहा.")}</span>
<div class="week">{"".join(f'<div class="day {"on" if i in days else ""} {"today" if i == today_idx() else ""}" style="--d:{i}"><i></i>{d}</div>' for i, d in enumerate(day_labels()))}</div></div>
<div class="ring"><svg viewBox="0 0 100 100"><circle class="bg" cx="50" cy="50" r="42"/><circle class="fg" cx="50" cy="50" r="42" style="--off:{off:.1f}"/></svg><span><b>{n}</b><small>{t("of 10 goal", "लक्ष्य 10", "ध्येय 10")}</small></span></div></div>''')
    with c2:
        w = TERM["Deepfake"]
        md(f'<div class="wotd"><span class="eyebrow">{t("Word of the day", "आज का शब्द", "आजचा शब्द")}</span><h3>{esc(L(w["name"]))}</h3><span>{esc(L(w["short"]))}</span></div>')
        st.button(t("Learn this word", "यह शब्द सीखें", "हा शब्द शिका"), icon=":material/arrow_forward:", on_click=open_term, args=("Deepfake",), key="wotd_btn")
    st.markdown(f"### {t('What would you like to do?', 'आप क्या करना चाहेंगे?', 'तुम्हाला काय करायला आवडेल?')}")
    tiles = [("ask", ":material/search:", t("Ask Before You Click", "क्लिक करने से पहले पूछें", "क्लिक करण्यापूर्वी विचारा"), t("Got a strange message? Check it before you tap anything.", "कोई अजीब संदेश आया? कुछ भी दबाने से पहले जांचें।", "विचित्र संदेश आला? काहीही दाबण्यापूर्वी तपासा.")),
             ("practice", ":material/verified_user:", t("Practice a Scenario", "अभ्यास करें", "सराव करा"), t("Try real-life situations safely — no penalty for mistakes.", "असली जैसी स्थितियों का सुरक्षित अभ्यास — गलती पर कोई सज़ा नहीं।", "खऱ्या आयुष्यातील प्रसंगांचा सुरक्षित सराव — चुकांसाठी शिक्षा नाही.")),
             ("recap", ":material/military_tech:", t("My Badges", "मेरे बैज", "माझे बॅज"), t(f"{len(S.badges)} badges earned — see what you’ve collected.", f"{len(S.badges)} बैज मिले — देखें आपने क्या कमाया।", f"{len(S.badges)} बॅज मिळाले — तुम्ही काय कमावले ते पाहा.")),
             ("learn", ":material/menu_book:", t("Learn Words", "शब्द सीखें", "शब्द शिका"), t("8 scam words explained in plain language.", "ठगी के 8 शब्द, आसान भाषा में।", "फसवणुकीचे 8 शब्द, सोप्या भाषेत."))]
    for i in range(0, 4, 2):
        cols = st.columns(2, gap="medium")
        for col, (pg, icon, a, b) in zip(cols, tiles[i:i + 2]):
            col.button(f"**{a}**  \n{b}", key=f"tile_{pg}", icon=icon, on_click=go, args=(pg,), use_container_width=True)
    recap_line = t(f"{S.checks} messages checked · {len(S.scen)} scenarios practised · {len(S.viewed)} words learned",
                   f"{S.checks} संदेश जांचे · {len(S.scen)} अभ्यास किए · {len(S.viewed)} शब्द सीखे",
                   f"{S.checks} संदेश तपासले · {len(S.scen)} सराव केले · {len(S.viewed)} शब्द शिकलात")
    if S.toggles["recap"]:
        recap_line += " · " + t("next recap on Sunday", "अगला सारांश रविवार को", "पुढचा सारांश रविवारी")
    st.button(f"**{t('This Week’s Recap', 'इस हफ्ते का सारांश', 'या आठवड्याचा सारांश')}**  \n{recap_line}", key="tile_recapwide", icon=":material/event_available:", on_click=go, args=("recap",), use_container_width=True)
    b1, b2 = st.columns([3, 1.2], vertical_alignment="center")
    md(b1, f'<div class="banner"><span class="ibox">{ic("chat")}</span><div><b>{t("Not sure about a call or message?", "किसी कॉल या संदेश को लेकर पक्का नहीं?", "एखाद्या कॉल किंवा संदेशाबद्दल खात्री नाही?")}</b><p>{t("Ask SafeStep Assistant — type your question.", "SafeStep सहायक से पूछें — अपना सवाल लिखें।", "SafeStep सहाय्यकाला विचारा — तुमचा प्रश्न लिहा.")}</p></div></div>')
    b2.button(t("Chat / Ask a question", "चैट करें / सवाल पूछें", "चॅट करा / प्रश्न विचारा"), type="primary", icon=":material/forum:", on_click=go, args=("assistant",), use_container_width=True)


def page_ask():
    header(t("Ask Before You Click", "क्लिक करने से पहले पूछें", "क्लिक करण्यापूर्वी विचारा"),
           t("Paste a message, link or describe a call — we’ll check it together.", "कोई संदेश, लिंक या कॉल के बारे में लिखें — हम साथ में जांचेंगे।", "संदेश, लिंक पेस्ट करा किंवा कॉलबद्दल लिहा — आपण मिळून तपासू."))
    with st.container(border=True):
        st.text_area(t("Paste or type the message you received", "जो संदेश आया है उसे चिपकाएं या लिखें", "आलेला संदेश पेस्ट करा किंवा लिहा"), key="ask_area", height=140,
                     placeholder=t("e.g. “Your account will be blocked today…”", "जैसे “आपका खाता आज बंद हो जाएगा…”", "उदा. “तुमचे खाते आज बंद होईल…”"))
        st.caption(t("Try an example:", "उदाहरण आज़माएं:", "एखादे उदाहरण वापरून पाहा:"))
        cols = st.columns([1, 1, 1, 1.2])
        for i, (label, text) in enumerate(EXAMPLES):
            cols[i].button(L(label), key=f"ex_{i}", on_click=lambda tx=text: S.update(ask_area=L(tx), ask_res=None), use_container_width=True)
        check = cols[3].button(t("Check it", "जांचें", "तपासा"), type="primary", icon=":material/search:", use_container_width=True)
    if check:
        text = (S.get("ask_area") or "").strip()
        if not text:
            st.warning(t("Paste or type a message first.", "पहले कोई संदेश चिपकाएं या लिखें।", "आधी एखादा संदेश पेस्ट करा किंवा लिहा."))
        else:
            with st.status(t("Checking…", "जांच रहे हैं…", "तपासत आहोत…"), expanded=True) as status:
                for s in [t("Looking for urgency and threats", "जल्दबाज़ी और धमकी ढूंढ रहे हैं", "घाई आणि धमक्या शोधत आहोत"), t("Checking links", "लिंक जांच रहे हैं", "लिंक तपासत आहोत"),
                          t("Checking requests for codes or PINs", "कोड या पिन की मांग जांच रहे हैं", "कोड किंवा पिनची मागणी तपासत आहोत"), t("Looking for money or prize bait", "पैसे या इनाम का चारा ढूंढ रहे हैं", "पैशाचे किंवा बक्षिसाचे आमिष शोधत आहोत")]:
                    st.write("✓ " + s); time.sleep(0.35)
                status.update(label=t("Done", "हो गया", "झाले"), state="complete", expanded=False)
            S.ask_res = analyze(text)
            S.checks += 1
    r = S.ask_res
    if r:
        lv = {"high": (t("Likely a scam", "संभवतः धोखाधड़ी", "बहुधा फसवणूक"), t("High risk", "ज़्यादा जोखिम", "जास्त धोका"), "red", ""),
              "mid": (t("Be careful with this one", "इसमें सावधान रहें", "याबाबत सावध राहा"), t("Some risk", "कुछ जोखिम", "थोडा धोका"), "amber", "mid"),
              "low": (t("Looks okay — still stay alert", "ठीक लगता है — फिर भी सावधान रहें", "ठीक वाटते — तरीही सावध राहा"), t("Low risk", "कम जोखिम", "कमी धोका"), "green", "low")}[r["level"]]
        keys = {f["k"] for f in r["flags"]}
        nxt = (t("Don’t share any code or PIN. If it claims to be your bank, call the number printed on your card.", "कोई भी कोड या पिन न बताएं। अगर यह बैंक होने का दावा करे, तो कार्ड पर छपे नंबर पर कॉल करें।", "कोणताही कोड किंवा पिन सांगू नका. बँक असल्याचा दावा केल्यास कार्डवर छापलेल्या नंबरवर कॉल करा.") if "code" in keys else
               t("Don’t click — open the official app or call your bank on the number on your card.", "क्लिक न करें — आधिकारिक ऐप खोलें या कार्ड पर लिखे नंबर पर बैंक को कॉल करें।", "क्लिक करू नका — अधिकृत ॲप उघडा किंवा कार्डवरील नंबरवर बँकेला कॉल करा.") if "link" in keys else
               t("Hang up. Real police never ask for money on a call. Visit your local police station if worried.", "फोन काटें। असली पुलिस कभी कॉल पर पैसे नहीं मांगती। चिंता हो तो पास के पुलिस स्टेशन जाएं।", "फोन ठेवा. खरे पोलीस कधीही कॉलवर पैसे मागत नाहीत. काळजी वाटल्यास जवळच्या पोलीस ठाण्यात जा.") if "threat" in keys else
               t("No common warning signs found. If anything still feels off, ask a family member before acting.", "कोई आम चेतावनी संकेत नहीं मिला। फिर भी कुछ अजीब लगे, तो कदम उठाने से पहले परिवार से पूछें।", "कोणतीही सामान्य धोक्याची चिन्हे आढळली नाहीत. तरीही काही खटकत असेल, तर काही करण्यापूर्वी कुटुंबाला विचारा.") if r["level"] == "low" else
               t("Pause before you act. Check with the company through its official app or helpline.", "कदम उठाने से पहले रुकें। कंपनी के आधिकारिक ऐप या हेल्पलाइन से जांच करें।", "काही करण्यापूर्वी थांबा. कंपनीच्या अधिकृत ॲप किंवा हेल्पलाइनवरून खात्री करा."))
        n = len(r["flags"])
        found = t(f"We found {n} warning sign{'s' if n != 1 else ''} in this message.", f"इस संदेश में हमें {n} चेतावनी संकेत मिले।", f"या संदेशात आम्हाला {n} धोक्याची चिन्हे आढळली.") if n else t("We didn’t find the usual warning signs.", "हमें आम चेतावनी संकेत नहीं मिले।", "आम्हाला नेहमीची धोक्याची चिन्हे आढळली नाहीत.")
        flags = "".join(f'<div class="flag" style="--i:{i}">{ic("warn")}<span><b>{esc(L(f["t"]))}</b><span class="muted">{esc(L(f["d"]))}</span></span></div>' for i, f in enumerate(r["flags"]))
        md(f'''<div class="verdict {lv[3]}"><div class="row"><span class="ibox {"red" if lv[2] == "red" else "amber" if lv[2] == "amber" else ""}" style="border-radius:50%">{ic("check" if r["level"] == "low" else "warn", "1.7em")}</span><div style="flex:1;min-width:12rem"><h2>{lv[0]}</h2><span class="muted">{found}</span></div><span class="pill {lv[2]}">{lv[1]}</span></div>
<div><span class="lab">{t("What we spotted in your message", "आपके संदेश में हमें यह मिला", "तुमच्या संदेशात आम्हाला हे आढळले")}</span><div class="quote">{highlight(r["text"], r["flags"])}</div></div>
{meter(r["pos"])}{f'<b>{t("Why we think so", "हमें ऐसा क्यों लगता है", "आम्हाला असे का वाटते")}</b>' + flags if flags else ""}</div>''')
        c1, c2 = st.columns([3, 1.2], vertical_alignment="center")
        md(c1, f'<div class="next"><span class="ibox" style="background:#fff;border-radius:50%">{ic("phone")}</span><div><span class="eyebrow">{t("What to do now", "अब क्या करें", "आता काय करावे")}</span><h3>{esc(nxt)}</h3></div></div>')
        c2.button(t("Ask the assistant", "सहायक से पूछें", "सहाय्यकाला विचारा"), icon=":material/forum:", on_click=go, args=("assistant",), use_container_width=True)
    else:
        how = [(t("Paste the message", "संदेश चिपकाएं", "संदेश पेस्ट करा"), t("Copy it from SMS, WhatsApp or email.", "SMS, WhatsApp या ईमेल से कॉपी करें।", "SMS, WhatsApp किंवा ईमेलमधून कॉपी करा.")),
               (t("We look for warning signs", "हम चेतावनी के संकेत ढूंढते हैं", "आम्ही धोक्याची चिन्हे शोधतो"), t("Urgency, strange links, requests for codes.", "जल्दबाज़ी, अजीब लिंक, कोड की मांग।", "घाई, विचित्र लिंक, कोडची मागणी.")),
               (t("You get one clear next step", "आपको एक साफ़ अगला कदम मिलता है", "तुम्हाला एक स्पष्ट पुढचे पाऊल मिळते"), t("No jargon — just what to do.", "कोई मुश्किल शब्द नहीं — बस क्या करना है।", "अवघड शब्द नाहीत — फक्त काय करायचे ते."))]
        md('<div class="how">' + "".join(f'<div><span class="num">{i + 1}</span><b>{a}</b><br><span class="muted">{b}</span></div>' for i, (a, b) in enumerate(how)) + "</div>")
    st.caption("🔒 " + t("Your message is checked inside SafeStep and is never stored or shared.", "आपका संदेश SafeStep के अंदर ही जांचा जाता है — न सेव होता है, न साझा।", "तुमचा संदेश SafeStep मध्येच तपासला जातो — तो साठवला किंवा शेअर केला जात नाही."))


def page_learn():
    header(t("Learn a Word", "एक शब्द सीखें", "एक शब्द शिका"),
           t("Eight scam words in plain language. Tap a word to learn it, then try 5 quick questions.", "आसान भाषा में ठगी के 8 शब्द। किसी शब्द पर टैप करें, फिर 5 झटपट सवाल आज़माएं।", "सोप्या भाषेत फसवणुकीचे 8 शब्द. शब्दावर टॅप करा आणि मग 5 झटपट प्रश्न सोडवा."))
    c1, c2 = st.columns([2, 1], vertical_alignment="bottom")
    q = c1.text_input(t("Search", "खोजें", "शोधा"), key="learn_q", placeholder=t("Search a word, e.g. “OTP”", "कोई शब्द खोजें, जैसे “OTP”", "शब्द शोधा, उदा. “OTP”"), label_visibility="collapsed")
    c2.progress(len(S.viewed) / 8, text=t(f"{len(S.viewed)} of 8 words viewed", f"8 में से {len(S.viewed)} शब्द देखे", f"8 पैकी {len(S.viewed)} शब्द पाहिले"))
    cats = {"all": ["All words", "सभी शब्द", "सर्व शब्द"], "Messages": ["Messages", "संदेश", "संदेश"], "Calls": ["Calls", "कॉल", "कॉल"], "Money": ["Money", "पैसा", "पैसा"], "Places": ["Places", "जगहें", "ठिकाणे"]}
    st.pills(t("Filter", "फ़िल्टर", "फिल्टर"), list(cats), format_func=lambda k: L(cats[k]), key="lf_ctl", default=S.lf, label_visibility="collapsed",
             on_change=lambda: S.update(lf=S.get("lf_ctl") or "all"))
    items = [x for x in TERMS if (S.lf == "all" or x["cat"][0] == S.lf) and (not q or q.lower() in " ".join(x["name"] + x["short"]).lower())]
    if not items:
        st.info(t("No word matches that search. Try “OTP” or “QR”.", "इस खोज से कोई शब्द नहीं मिला। “OTP” या “QR” आज़माएं।", "या शोधाशी जुळणारा शब्द नाही. “OTP” किंवा “QR” वापरून पाहा."))
    for r in range(0, len(items), 4):
        cols = st.columns(4, gap="small")
        for j, (col, x) in enumerate(zip(cols, items[r:r + 4])):
            done = S.quiz.get(x["key"], {}).get("done")
            badge = (f'<span class="pill green">{ic("check", "1em")}{t("Quiz done", "सवाल पूरे", "प्रश्न पूर्ण")}</span>' if done else
                     f'<span class="pill green">{ic("check", "1em")}{t("Viewed", "देखा", "पाहिले")}</span>' if x["key"] in S.viewed else "")
            with col:
                md(f'<div class="term" style="--i:{r + j}"><div class="top"><span class="ibox" style="width:3.1rem;height:3.1rem;border-radius:15px">{ic(x["icon"], "1.5em")}</span>{badge}</div><small class="muted">{esc(L(x["cat"]))}</small><h3>{esc(L(x["name"]))}</h3><span class="muted" style="font-size:.97rem">{esc(L(x["short"]))}</span></div>')
                st.button(t("Learn · 5 questions", "सीखें · 5 सवाल", "शिका · 5 प्रश्न"), key=f"learn_{x['key']}", icon=":material/arrow_forward:", on_click=open_term, args=(x["key"],), use_container_width=True)
    st.caption("💡 " + t("Words you view here shape your weekly “Did you know?” fact.", "यहां देखे गए शब्दों से आपके साप्ताहिक “क्या आप जानते हैं?” तथ्य तय होते हैं।", "इथे पाहिलेल्या शब्दांवरून तुमचे साप्ताहिक “तुम्हाला माहीत आहे का?” ठरते."))


def scen_status(key: str) -> str:
    v = S.scen.get(key)
    if not v:
        return "○ " + t("New", "नया", "नवीन")
    return "✓ " + t("Spotted on first try", "पहली बार में पहचाना", "पहिल्याच प्रयत्नात ओळखले") if v["first"] else "↺ " + t("Worth another look", "एक बार और देखें", "पुन्हा एकदा पाहण्यासारखे")


SC_ICON = {"phone": ":material/call:", "sms": ":material/sms:", "qr": ":material/qr_code_2:", "warn": ":material/warning:", "coin": ":material/payments:", "video": ":material/videocam:"}


def page_practice():
    header(t("Practice a Scenario", "अभ्यास करें", "सराव करा"),
           t("Real-life situations, safely. Choose what you’d do — mistakes are part of practice.", "असली जैसी स्थितियां, सुरक्षित तरीके से। चुनें कि आप क्या करेंगे — गलतियां अभ्यास का हिस्सा हैं।", "खऱ्या आयुष्यातील प्रसंग, सुरक्षितपणे. तुम्ही काय कराल ते निवडा — चुका हा सरावाचाच भाग आहे."))
    n = len(S.scen)
    c1, c2 = st.columns([1.2, 2], vertical_alignment="center")
    c1.progress(n / 7, text=t(f"{n} of 7 practised", f"7 में से {n} का अभ्यास", f"7 पैकी {n} सराव केले"))
    md(c2, '<div class="row" style="gap:.5rem;justify-content:flex-end">' + "".join(f'<span class="pill amber">{ic("badge", "1em")}{esc(b)}</span>' for b in S.badges[:5]) + "</div>")
    f = {"all": ["All", "सभी", "सर्व"], "new": ["New", "नए", "नवीन"], "first": ["Spotted first try", "पहली बार में सही", "पहिल्याच प्रयत्नात बरोबर"], "again": ["Worth another look", "एक बार और देखें", "पुन्हा एकदा पाहण्यासारखे"]}
    a, b = st.columns([3, 1], vertical_alignment="center")
    with a:
        st.pills(t("Filter", "फ़िल्टर", "फिल्टर"), list(f), format_func=lambda k: L(f[k]), key="pf_ctl", default=S.pf, label_visibility="collapsed",
                 on_change=lambda: S.update(pf=S.get("pf_ctl") or "all"))

    def surprise():
        fresh = [i for i, s in enumerate(SCEN) if s["key"] not in S.scen] or list(range(len(SCEN)))
        go("scenario", scen_idx=random.choice(fresh))
    b.button(t("Surprise me", "कोई भी चुनें", "कोणताही निवडा"), icon=":material/shuffle:", on_click=surprise, use_container_width=True)
    shown = [(i, s) for i, s in enumerate(SCEN) if S.pf == "all" or (S.pf == "new" and s["key"] not in S.scen)
             or (S.pf == "first" and S.scen.get(s["key"], {}).get("first") is True) or (S.pf == "again" and S.scen.get(s["key"], {}).get("first") is False)]
    if not shown:
        st.info(t("Nothing here yet — try another filter.", "यहां अभी कुछ नहीं — कोई और फ़िल्टर आज़माएं।", "इथे अजून काही नाही — दुसरा फिल्टर वापरून पाहा."))
    for r in range(0, len(shown), 2):
        cols = st.columns(2, gap="medium")
        for col, (i, s) in zip(cols, shown[r:r + 2]):
            col.button(f"**{L(s['name'])}**  \n{L(s['teaser'])}  \n{scen_status(s['key'])}", key=f"tile_sc{i}", icon=SC_ICON.get(s["icon"], ":material/shield:"),
                       on_click=go, args=("scenario",), kwargs={"scen_idx": i}, use_container_width=True)
    st.caption("💡 " + t("Scenarios you needed a second look at are gently suggested again in your Weekly Recap.", "जिन परिदृश्यों में दोबारा देखना पड़ा, वे आपके साप्ताहिक सारांश में फिर से सुझाए जाते हैं।", "ज्या प्रसंगांत पुन्हा पाहावे लागले, ते तुमच्या साप्ताहिक सारांशात पुन्हा सुचवले जातात."))


GAMES_FILE = Path(__file__).parent / "games" / "mini-games.html"


def games_html(code: str) -> str:
    """The three mini games, set to the app's language. The game's own title and
    language buttons are hidden because the app already shows them."""
    src = GAMES_FILE.read_text(encoding="utf-8")
    extra = (f"<script>window.SAFESTEP_LANG = {json.dumps(code)};</script>"
             "<style>#title, .lang-row [data-lang] { display: none !important; }</style>")
    return src.replace("<head>", "<head>" + extra, 1)


def page_games():
    header(t("Mini Games", "मिनी गेम्स", "मिनी गेम्स"),
           t("Learn to spot scams through play — three short games, no quizzes.",
             "खेल-खेल में ठगी पहचानना सीखें — तीन छोटे गेम, कोई क्विज़ नहीं।",
             "खेळता खेळता फसवणूक ओळखायला शिका — तीन छोटे खेळ, प्रश्नमंजूषा नाही."))
    if not GAMES_FILE.exists():
        st.error(t("The games file is missing (games/mini-games.html).", "गेम्स की फ़ाइल नहीं मिली (games/mini-games.html)।", "खेळांची फाइल सापडली नाही (games/mini-games.html)."))
        return
    components.html(games_html(lang()), height=1300, scrolling=True)
    st.caption("💡 " + t("Your game progress is saved on this device.", "आपकी गेम प्रगति इसी डिवाइस पर सेव होती है।", "तुमची खेळातील प्रगती याच डिव्हाइसवर जतन होते."))


def page_scenario():
    i = S.scen_idx % len(SCEN)
    s = SCEN[i]
    header(L(s["name"]), t(f"Scenario {i + 1} of 7", f"परिदृश्य {i + 1} / 7", f"प्रसंग {i + 1} / 7"))
    st.button(t("All scenarios", "सभी परिदृश्य", "सर्व प्रसंग"), icon=":material/arrow_back:", type="tertiary", on_click=go, args=("practice",))
    md(f'<div class="situation"><span class="ibox">{ic(s["icon"], "1.8em")}</span><div><span class="eyebrow">{t("The situation", "स्थिति", "परिस्थिती")}</span><p>{esc(L(s["sit"]))}</p></div></div>')
    st.markdown(f"#### {t('What would you do?', 'आप क्या करेंगे?', 'तुम्ही काय कराल?')}")
    pick = S.pick.get(i)

    def choose(letter):
        S.pick = {i: letter}
        S.reveal = False
        ok = letter == s["c"]
        S.scen.setdefault(s["key"], {"first": ok})
        if ok:
            S.celebrate = s["badge"] not in S.badges
            if s["badge"] not in S.badges:
                S.badges.append(s["badge"])
    for letter in ("A", "B"):
        txt = L(s[letter.lower()])
        if pick is None:
            st.button(f"**{letter}** · {txt}", key=f"choice_s{i}{letter}", on_click=choose, args=(letter,), use_container_width=True)
        else:
            ok = pick == s["c"]
            cls = ("correct" if letter == s["c"] else "dim") if ok else ("wrong" if letter == pick else ("safer" if S.reveal else ""))
            md(f'<div class="picked {cls or "dim"}" style="{"" if cls else "opacity:1;border:1.5px solid var(--field)"}"><span class="L">{letter}</span><span style="flex:1">{esc(txt)}</span>{ic("check") if cls in ("correct", "safer") else ""}</div>')
    if pick is None:
        st.caption("💡 " + t("Take your time — there’s no timer and no score.", "आराम से सोचें — कोई टाइमर नहीं, कोई नंबर नहीं।", "निवांत विचार करा — टायमर नाही, गुण नाहीत."))
        return
    if pick == s["c"]:
        bdg = s["badge"]
        won = t(f"You earned the “{bdg}” badge", f"आपको “{bdg}” बैज मिला", f"तुम्हाला “{bdg}” बॅज मिळाला")
        md(f'<div class="fb ok">{ic("check")}<span><b>{t("Good instinct!", "बढ़िया समझ!", "छान ओळखलेत!")}</b>{esc(L(s["ok"]))}</span></div>'
                f'<div class="badge-won"><span class="medal">{ic("badge", "1.8em")}</span><span><b style="font-size:1.15rem;display:block">{won}</b><span class="muted">{t("You’re doing great — one more safe decision under your belt.", "आप बढ़िया कर रहे हैं — एक और सुरक्षित फैसला आपके नाम।", "तुम्ही छान करत आहात — आणखी एक सुरक्षित निर्णय तुमच्या नावावर.")}</span></span></div>')
        if S.celebrate:
            st.balloons(); S.celebrate = False
    else:
        md(f'<div class="fb no">{ic("bulb")}<span><b>{t("Let’s look closer.", "आइए ध्यान से देखें।", "चला, नीट पाहूया.")}</b>{esc(L(s["no"]))}</span></div>')
        if not S.reveal:
            st.button(t("See the safer choice", "सुरक्षित विकल्प देखें", "सुरक्षित पर्याय पाहा"), icon=":material/shield:", on_click=lambda: S.update(reveal=True))
            return
        md(f'<div class="safer-box">{ic("shield", "1.6em", "#0F5E4E")}<span><span class="eyebrow">{t("The safer choice", "सुरक्षित विकल्प", "सुरक्षित पर्याय")}</span><b style="display:block;font-size:1.12rem">{esc(L(s[s["c"].lower()]))}</b></span></div>')
        st.caption(t("It’s okay — this is exactly what practicing is for.", "कोई बात नहीं — अभ्यास इसी के लिए होता है।", "काही हरकत नाही — सराव यासाठीच असतो."))
    c1, c2, _ = st.columns([1.3, 1.2, 2])
    c1.button(t("Try another scenario", "दूसरा परिदृश्य आज़माएं", "दुसरा प्रसंग करून पाहा"), type="primary", icon=":material/arrow_forward:", on_click=go, args=("scenario",), kwargs={"scen_idx": (i + 1) % 7})
    c2.button(t("Try this one again", "इसे फिर से आज़माएं", "हाच पुन्हा करून पाहा"), icon=":material/replay:", on_click=lambda: S.update(pick={}, reveal=False))


def page_recap():
    header(t("My Weekly Recap", "मेरा साप्ताहिक सारांश", "माझा साप्ताहिक सारांश"), t("Your Safety Week", "आपका सुरक्षा सप्ताह", "तुमचा सुरक्षा आठवडा"))
    stats = [(S.checks, t("messages checked", "संदेश जांचे", "संदेश तपासले"), "search", ""), (len(S.scen), t("scenarios practised", "अभ्यास किए", "सराव केले"), "play", ""),
             (len(S.viewed), t("words learned", "शब्द सीखे", "शब्द शिकलात"), "book", ""), (len(S.badges), t("badges earned", "बैज मिले", "बॅज मिळाले"), "badge", "amber")]
    cols = st.columns(4, gap="small")
    for col, (n, label, icon, c) in zip(cols, stats):
        md(col, f'<div class="stat {c}"><span class="ibox {c}">{ic(icon, "1.6em")}</span><span><b style="animation:popIn .5s var(--ease) backwards">{n}</b><span class="muted">{label}</span></span></div>')
    first = [s for s in SCEN if S.scen.get(s["key"], {}).get("first") is True]
    second = [s for s in SCEN if S.scen.get(s["key"], {}).get("first") is False]
    join = t(" and ", " और ", " आणि ")
    names = lambda arr: join.join(L(s["name"]) for s in arr)
    left, right = st.columns([1.7, 1], gap="medium")
    with left:
        with st.container(border=True):
            st.markdown(f"#### ✨ {t('Your Week in Review', 'आपके हफ्ते की झलक', 'तुमच्या आठवड्याचा आढावा')}")
            line = t(f"You checked {S.checks} messages this week.", f"इस हफ्ते आपने {S.checks} संदेश जांचे।", f"या आठवड्यात तुम्ही {S.checks} संदेश तपासले.")
            if first:
                line += " " + t(f"You got {names(first)} right on your first try — calm, careful choices.", f"आपने {names(first)} पहली बार में सही किए — शांत और सोच-समझकर लिए फैसले।", f"{names(first)} तुम्ही पहिल्याच प्रयत्नात बरोबर केले — शांत, विचारपूर्वक निर्णय.")
            st.markdown(line)
            if second:
                rev = TERM[SCEN_TERM[second[0]["key"]]]
                st.markdown(t(f"{names(second)} took a second look, so {L(rev['name']).lower()} is a good one to revisit this week.", f"{names(second)} में दोबारा देखना पड़ा, इसलिए इस हफ्ते {L(rev['name'])} को फिर से देखना अच्छा रहेगा।", f"{names(second)} मध्ये पुन्हा पाहावे लागले, म्हणून या आठवड्यात {L(rev['name'])} पुन्हा पाहणे चांगले."))
                b1, b2 = st.columns(2)
                b1.button(t(f"Revisit {L(rev['name'])}", f"{L(rev['name'])} दोबारा देखें", f"{L(rev['name'])} पुन्हा पाहा"), icon=":material/menu_book:", on_click=open_term, args=(rev["key"],), use_container_width=True)
                b2.button(t(f"Try {L(second[0]['name'])} again", f"{L(second[0]['name'])} फिर आज़माएं", f"{L(second[0]['name'])} पुन्हा करून पाहा"), icon=":material/replay:",
                          on_click=go, args=("scenario",), kwargs={"scen_idx": SCEN.index(second[0])}, use_container_width=True)
            else:
                st.caption(t("Nothing to revisit — every scenario so far was spotted on the first try.", "दोबारा देखने को कुछ नहीं — अब तक हर परिदृश्य पहली बार में पहचाना गया।", "पुन्हा पाहण्यासारखे काही नाही — आतापर्यंतचा प्रत्येक प्रसंग पहिल्याच प्रयत्नात ओळखला."))
        with st.container(border=True):
            st.markdown(f"**{t('You learned:', 'आपने सीखा:', 'तुम्ही शिकलात:')}** " + ", ".join(L(TERM[k]["name"]) for k in S.viewed))
            st.button(t("Read more", "और पढ़ें", "आणखी वाचा"), type="primary", icon=":material/arrow_forward:", on_click=go, args=("learn",))
    with right:
        days = set(S.days) | {today_idx()}
        week_html = "".join('<div class="day %s" style="--d:%d"><i style="border-color:var(--field)"></i>%s</div>' % ("on" if i in days else "", i, d) for i, d in enumerate(day_labels()))
        md(f'<div class="card"><b>{t("Active this week:", "इस हफ्ते सक्रिय:", "या आठवड्यात सक्रिय:")}</b><div class="week">{week_html}</div></div>')
        fk = S.last_viewed if S.last_viewed in FACTS else None
        md(f'<div class="dyk"><b style="display:flex;gap:.5rem;align-items:center;font-size:1.12rem">{ic("bulb")}{t("Did you know?", "क्या आप जानते हैं?", "तुम्हाला माहीत आहे का?")}</b><p style="margin:.5rem 0">{esc(L(FACTS[fk]) if fk else L(FALLBACK_FACT))}</p>'
                + (f'<span class="pill amber" style="background:#fff">{t("Because you viewed:", "क्योंकि आपने देखा:", "कारण तुम्ही पाहिले:")} {esc(L(TERM[fk]["name"]))}</span>' if fk else "") + "</div>")
    with st.container(border=True):
        st.markdown(f"#### 🏅 {t('Badges you’ve earned', 'आपके बैज', 'तुम्हाला मिळालेले बॅज')}")
        md('<div class="medals">' + "".join(f'<div class="{"" if b in S.badges else "off"}" style="--i:{i}"><span class="medal">{ic("badge", "1.6em")}</span>“{esc(b)}”</div>' for i, b in enumerate(ALL_BADGES)) + "</div>")
        with st.popover(t("How do I earn badges?", "बैज कैसे मिलते हैं?", "बॅज कसे मिळतात?"), icon=":material/help:"):
            for sc in SCEN:
                st.markdown(f"{'🏅' if sc['badge'] in S.badges else '○'} **{sc['badge']}** — {L(sc['name'])}")
            st.markdown(f"{'🏅' if 'Word Wise' in S.badges else '○'} **Word Wise** — {t('finish all 5 questions for any word', 'किसी भी शब्द के सभी 5 सवाल पूरे करें', 'कोणत्याही शब्दाचे सर्व 5 प्रश्न पूर्ण करा')}")
    with st.container(border=True):
        st.toggle(t("Share this recap with my daughter Priya", "यह सारांश मेरी बेटी प्रिया के साथ साझा करें", "हा सारांश माझी मुलगी प्रियासोबत शेअर करा"), value=S.shared, key="share_ctl",
                  on_change=lambda: (S.update(shared=S.share_ctl), flash(t("Recap shared with Priya", "सारांश प्रिया के साथ साझा किया", "सारांश प्रियासोबत शेअर केला") if S.share_ctl else t("Sharing stopped", "साझा करना बंद किया", "शेअर करणे थांबवले"), "👨‍👩‍👧")))
        st.caption(t("Only when you choose. Priya gets a short summary — never your messages.", "सिर्फ आपकी मर्ज़ी से। प्रिया को एक छोटा सारांश मिलेगा — आपके संदेश कभी नहीं।", "फक्त तुमच्या इच्छेने. प्रियाला छोटा सारांश मिळेल — तुमचे संदेश कधीच नाहीत."))


def ai_meta_html(r: dict) -> str:
    pos = {"low": .2, "medium": .55, "high": .88}.get(r.get("risk"))
    pill = {"low": ("green", t("Low risk", "कम जोखिम", "कमी धोका")), "medium": ("amber", t("Some risk", "कुछ जोखिम", "थोडा धोका")), "high": ("red", t("High risk", "ज़्यादा जोखिम", "जास्त धोका"))}.get(r.get("risk"))
    out = ""
    if pos:
        out += f'<div class="row" style="gap:.5rem;margin:.3rem 0"><span class="lab">{t("Risk meter", "जोखिम मीटर", "धोका मीटर")}</span><span class="pill {pill[0]}">{pill[1]}</span></div>{meter(pos)}'
    if r.get("next_step"):
        out += f'<div class="box tip" style="margin-top:.7rem">{ic("shield")}<span><b>{t("Next step", "अगला कदम", "पुढचे पाऊल")}:</b> {esc(r["next_step"])}</span></div>'
    return out


def page_assistant():
    header(t("SafeStep Assistant", "SafeStep सहायक", "SafeStep सहाय्यक"),
           t("Ask anything about a call, message or link.", "किसी कॉल, संदेश या लिंक के बारे में कुछ भी पूछें।", "कॉल, संदेश किंवा लिंकबद्दल काहीही विचारा."))
    live = assistant.ai_enabled()
    side, main = st.columns([1, 2.2], gap="medium")
    asked = None
    with side:
        md(f'<span class="pill {"green" if live else "sand"}">{ic("spark", "1em") if live else ""}{t("Live AI assistant", "लाइव AI सहायक", "लाइव्ह AI सहाय्यक") if live else t("Built-in answers", "बिल्ट-इन जवाब", "अंगभूत उत्तरे")}</span>')
        st.markdown(f"**{t('You can ask me things like…', 'आप मुझसे ऐसी बातें पूछ सकते हैं…', 'तुम्ही मला असे विचारू शकता…')}**")
        for i, p in enumerate([t("Is this call safe? Someone asked for my OTP.", "क्या यह कॉल सुरक्षित है? किसी ने मेरा OTP मांगा।", "हा कॉल सुरक्षित आहे का? कोणीतरी माझा OTP मागितला."),
                               t("What is vishing?", "विशिंग क्या है?", "व्हिशिंग म्हणजे काय?"), t("How do I check a QR code?", "QR कोड कैसे जांचें?", "QR कोड कसा तपासायचा?")]):
            if st.button(p, key=f"prompt_{i}", use_container_width=True):
                asked = p
        if st.button(t("Start a new chat", "नई चैट शुरू करें", "नवीन चॅट सुरू करा"), icon=":material/refresh:", type="tertiary"):
            S.chat = []; st.rerun()
        st.caption("🔒 " + t("I never ask for your OTP, PIN or bank details.", "मैं कभी आपका OTP, पिन या बैंक जानकारी नहीं मांगता।", "मी कधीही तुमचा OTP, पिन किंवा बँक माहिती मागत नाही.")
                   + (" " + t("Your questions go to our AI service to be answered, so please don’t type codes or passwords.", "आपके सवाल जवाब के लिए हमारी AI सेवा को भेजे जाते हैं, इसलिए कोड या पासवर्ड न लिखें।", "तुमचे प्रश्न उत्तरासाठी आमच्या AI सेवेकडे पाठवले जातात, म्हणून कोड किंवा पासवर्ड लिहू नका.") if live else ""))
    with main:
        box = st.container(height=480, border=True)
        with box:
            with st.chat_message("assistant", avatar=":material/shield:"):
                st.markdown(t("Namaste Meena! I’m your SafeStep Assistant. Tell me what happened — I’ll help you check it.", "नमस्ते मीना! मैं आपका SafeStep सहायक हूं। बताइए क्या हुआ — मैं जांचने में मदद करूंगा।", "नमस्कार मीना! मी तुमचा SafeStep सहाय्यक आहे. काय झाले ते सांगा — मी तपासायला मदत करेन."))
            for k, m in enumerate(S.chat):
                render_msg(k, m)
        typed = st.chat_input(t("Type your question", "अपना सवाल लिखें", "तुमचा प्रश्न लिहा"))
    q = (typed or asked or "").strip()
    if q:
        S.chat.append({"role": "user", "content": q})
        now = time.time()
        S.chat_times = [x for x in S.chat_times if now - x < 3600] + [now]
        with box:
            render_msg(len(S.chat) - 1, S.chat[-1])
            with st.chat_message("assistant", avatar=":material/shield:"):
                with st.spinner(t("Thinking…", "सोच रहा हूं…", "विचार करत आहे…")):
                    note = ""
                    if live and len(S.chat_times) <= 40:
                        try:
                            hist = [{"role": m["role"], "content": m["content"]} for m in S.chat]
                            r = assistant.run_agent(lang(), hist)
                        except Exception as e:
                            print("[chat]", repr(e), flush=True)
                            r = assistant.offline_reply(q)
                            note = t("I couldn’t reach the AI right now, so here’s a quick offline answer.", "अभी AI से जुड़ नहीं पाए, इसलिए यह एक छोटा ऑफ़लाइन जवाब है।", "आत्ता AI शी जोडता आले नाही, म्हणून हे छोटे ऑफलाइन उत्तर आहे.")
                    else:
                        time.sleep(0.6)
                        r = assistant.offline_reply(q)
        S.chat.append({"role": "assistant", "content": (r.get("reply") or "") + ("\n" + r["next_step"] if r.get("next_step") else ""), "meta": r, "note": note})
        st.rerun()


def render_msg(k: int, m: dict):
    if m["role"] == "user":
        with st.chat_message("user", avatar=":material/person:"):
            st.markdown(esc(m["content"]))
        return
    r = m.get("meta", {})
    with st.chat_message("assistant", avatar=":material/shield:"):
        if m.get("note"):
            st.caption(m["note"])
        st.markdown(esc(r.get("reply", "")))
        meta = ai_meta_html(r)
        if meta:
            md(meta)
        cols = st.columns(2)
        if r.get("show_help_button"):
            cols[0].button(t("Get help now", "अभी मदद पाएं", "आत्ता मदत घ्या"), key=f"chelp_{k}", icon=":material/support:", on_click=go, args=("help",))
        if r.get("related_term") in TERM:
            cols[1].button(L(TERM[r["related_term"]]["name"]), key=f"cterm_{k}", icon=":material/menu_book:", on_click=open_term, args=(r["related_term"],))


def page_help():
    header(t("Need help right now?", "अभी मदद चाहिए?", "आत्ता मदत हवी आहे?"),
           t("Stay calm. You’re not in trouble — follow these 3 steps.", "शांत रहें। आप मुसीबत में नहीं हैं — ये 3 कदम उठाएं।", "शांत राहा. तुम्ही अडचणीत नाही — या 3 पायऱ्या करा."), show_help=False)
    k = len(S.help_done)
    st.progress(k / 3, text=t(f"{k} of 3 steps done", f"3 में से {k} कदम पूरे", f"3 पैकी {k} पायऱ्या पूर्ण"))
    steps = [("1", "phone", t("Stop and hang up", "रुकें और फोन काटें", "थांबा आणि फोन ठेवा"), t("Don’t share any more details, codes or money. It’s okay to end the call.", "कोई और जानकारी, कोड या पैसा साझा न करें। कॉल खत्म करना बिल्कुल ठीक है।", "आणखी कोणतीही माहिती, कोड किंवा पैसे देऊ नका. कॉल बंद करणे अगदी योग्य आहे."), ""),
             ("2", "card", t("Call your bank", "अपने बैंक को कॉल करें", "तुमच्या बँकेला कॉल करा"), t("Use the number on your card or bank app to block your card and stop payments.", "कार्ड या बैंक ऐप पर लिखे नंबर से कार्ड ब्लॉक करवाएं और भुगतान रुकवाएं।", "कार्ड किंवा बँक ॲपवरील नंबरवर कॉल करून कार्ड ब्लॉक करा आणि व्यवहार थांबवा."), ""),
             ("3", "shield", t("Report it on 1930", "1930 पर शिकायत करें", "1930 वर तक्रार करा"), t("Call the national cyber crime helpline, or report at cybercrime.gov.in.", "राष्ट्रीय साइबर अपराध हेल्पलाइन पर कॉल करें, या cybercrime.gov.in पर शिकायत दर्ज करें।", "राष्ट्रीय सायबर गुन्हे हेल्पलाइनला कॉल करा, किंवा cybercrime.gov.in वर तक्रार नोंदवा."), "r")]
    cols = st.columns(3, gap="medium")

    def toggle(n):
        S.help_done = [x for x in S.help_done if x != n] if n in S.help_done else S.help_done + [n]
        if len(S.help_done) == 3:
            flash(t("Well done — you’ve taken every step.", "शाबाश — आपने हर कदम उठा लिया।", "शाब्बास — तुम्ही सर्व पायऱ्या पूर्ण केल्या."), "🛡️")
    for col, (n, icon, a, b, r) in zip(cols, steps):
        with col:
            md(f'<div class="step {"isdone" if n in S.help_done else ""}"><div class="row"><span class="bignum {r}">{n}</span>{ic(icon, "1.5em", "#B4432F" if r else "#0F5E4E")}</div><h3>{a}</h3><span class="muted">{b}</span></div>')
            if n == "3":
                st.code("1930", language=None)
            st.checkbox(t("Done", "हो गया", "झाले"), value=n in S.help_done, key=f"hd_{n}", on_change=toggle, args=(n,))
    c1, c2, c3 = st.columns([1, 1.3, 1.3])
    with c1:
        st.link_button(t("Call 1930", "1930 पर कॉल करें", "1930 वर कॉल करा"), "tel:1930", icon=":material/call:", key="call1930", use_container_width=True)
    c2.link_button("cybercrime.gov.in", "https://cybercrime.gov.in", icon=":material/open_in_new:", use_container_width=True)
    c3.link_button(t("Call Priya (daughter)", "प्रिया (बेटी) को कॉल करें", "प्रिया (मुलगी) ला कॉल करा"), "tel:+919820011223", icon=":material/family_restroom:", use_container_width=True)
    st.success(t("Reporting quickly gives the best chance of stopping a payment. Scams happen to careful people too — you did the right thing by acting.", "जल्दी शिकायत करने से भुगतान रुकने की संभावना सबसे ज़्यादा होती है। ठगी सावधान लोगों के साथ भी होती है — कदम उठाकर आपने सही किया।", "लवकर तक्रार केल्याने व्यवहार थांबवण्याची शक्यता सर्वाधिक असते. सावध लोकांचीही फसवणूक होते — पाऊल उचलून तुम्ही योग्य केले."), icon=":material/shield:")
    st.button(t("I’m safe now — back to Home", "अब मैं सुरक्षित हूं — होम पर जाएं", "आता मी सुरक्षित आहे — होमवर परत जा"), icon=":material/home:", on_click=go, args=("home",))


def page_account():
    header(t("My Account", "मेरा खाता", "माझे खाते"), t("Your details and how SafeStep looks for you.", "आपकी जानकारी और SafeStep आपके लिए कैसा दिखे।", "तुमची माहिती आणि SafeStep तुम्हाला कसे दिसावे."))
    left, right = st.columns([1, 2], gap="medium")
    with left:
        md(f'<div class="card" style="text-align:center;display:grid;justify-items:center;gap:.3rem"><span class="avatar" style="width:5rem;height:5rem;font-size:2rem">M</span><b style="font-size:1.3rem">{t("Meena Sharma", "मीना शर्मा", "मीना शर्मा")}</b><span class="muted">{mask_phone()}</span><small class="muted">{t("Trusted family contact: Priya (daughter)", "भरोसेमंद परिवार सदस्य: प्रिया (बेटी)", "विश्वासू कुटुंबातील व्यक्ती: प्रिया (मुलगी)")}</small></div>')

        def logout():
            for k in ("chat", "chat_times"):
                S[k] = []
            S.authed, S.otp_stage, S.page = False, "phone", "home"
        st.button(t("Log out", "लॉग आउट करें", "लॉग आउट करा"), icon=":material/logout:", on_click=logout, use_container_width=True)
    with right:
        with st.container(border=True):
            st.markdown(f"**🌐 {t('Language', 'भाषा', 'भाषा')}** — {t('changes the whole app instantly', 'पूरा ऐप तुरंत बदल जाता है', 'संपूर्ण ॲप लगेच बदलते')}")
            lang_switch("account")
            st.markdown(f"**🔠 {t('Text size', 'अक्षरों का आकार', 'अक्षरांचा आकार')}**")
            st.segmented_control("size", [0, 1, 2], format_func=lambda i: ["A", "A+", "A++"][i], key="size_ctl", default=S.size, required=True, label_visibility="collapsed",
                                 on_change=lambda: S.update(size=S.size_ctl))
            st.divider()
            labels = {"recap": t("Weekly recap every Sunday", "हर रविवार साप्ताहिक सारांश", "दर रविवारी साप्ताहिक सारांश"),
                      "tip": t("Daily safety tip in the menu", "मेन्यू में रोज़ की सुरक्षा टिप", "मेनूमध्ये रोजची सुरक्षा टीप"),
                      "alerts": t("Alerts about new scams on Home", "होम पर नई ठगी के अलर्ट", "होमवर नवीन फसवणुकींचे इशारे")}
            for k, label in labels.items():
                st.toggle(label, value=S.toggles[k], key=f"tg_{k}", on_change=lambda k=k: S.toggles.update({k: S[f"tg_{k}"]}))
            st.divider()
            st.markdown(f"**{t('Start my progress fresh', 'मेरी प्रगति नए सिरे से शुरू करें', 'माझी प्रगती नव्याने सुरू करा')}**")
            if not S.confirm_reset:
                st.button(t("Reset", "रीसेट करें", "रीसेट करा"), icon=":material/restart_alt:", on_click=lambda: S.update(confirm_reset=True))
            else:
                st.warning(t("Are you sure? This clears your practice history.", "पक्का? इससे आपका अभ्यास इतिहास हट जाएगा।", "नक्की? यामुळे तुमचा सराव इतिहास पुसला जाईल."))
                c1, c2, _ = st.columns([1, 1, 2])

                def do_reset():
                    S.update(viewed=[], last_viewed=None, scen={}, badges=[], checks=0, days=[], quiz={}, help_done=[], confirm_reset=False, ask_res=None, chat=[])
                    flash(t("Progress cleared", "प्रगति हटा दी गई", "प्रगती पुसली"), "🧹")
                c1.button(t("Yes, reset", "हां, रीसेट करें", "हो, रीसेट करा"), type="primary", on_click=do_reset)
                c2.button(t("Cancel", "रद्द करें", "रद्द करा"), on_click=lambda: S.update(confirm_reset=False))


# ------------------------------------------------------------------ router
PAGES = {"home": page_home, "ask": page_ask, "learn": page_learn, "practice": page_practice, "games": page_games, "scenario": page_scenario,
         "recap": page_recap, "assistant": page_assistant, "help": page_help, "account": page_account}


CLOSE_MENU_JS = """<script>(function(){if(window.innerWidth>=768)return;setTimeout(function(){
var s=document.querySelector('section[data-testid="stSidebar"]');if(!s||s.getBoundingClientRect().right<=0)return;
var b=document.querySelector('[data-testid="stSidebarCollapseButton"] button')||document.querySelector('[data-testid="stSidebarCollapseButton"]');if(b)b.click();},150);})();</script>"""


def make_page(key: str):
    def run():
        if S.get("_shown_page") != key:      # on phones, close the menu after choosing a page
            S._shown_page = key
            st.html(CLOSE_MENU_JS, unsafe_allow_javascript=True)
        S.page = key
        page_key = key if key != "scenario" else f"scenario{S.scen_idx}"
        with st.container(key=f"page_{page_key}"):   # new key per page → entrance animation replays
            PAGES[key]()
        if S.term_open:
            term_dialog(S.term_open)
    return run


if S.flash:
    st.toast(S.flash[0], icon=S.flash[1])
    S.flash = None

st.logo("assets/logo.png", size="large", icon_image="assets/icon.png")
if not S.authed:
    def login_page():
        with st.container(key="page_login"):
            page_login()
    nav = st.navigation([st.Page(login_page, title="SafeStep", icon=":material/shield:", url_path="signin")], position="hidden")
else:
    pages = {key: st.Page(make_page(key), title=L(label), icon=icon, url_path=key, default=(key == "home")) for key, icon, label in NAV}
    pages["scenario"] = st.Page(make_page("scenario"), title=t("Scenario", "परिदृश्य", "प्रसंग"), icon=":material/verified_user:", url_path="scenario", visibility="hidden")
    pages["help"] = st.Page(make_page("help"), title=t("Need Help Now?", "अभी मदद चाहिए?", "आत्ता मदत हवी आहे?"), icon=":material/support:", url_path="help", visibility="hidden")
    nav = st.navigation(list(pages.values()), position="sidebar")
    if S.goto:
        target, S.goto = S.goto, None
        st.switch_page(pages[target])
    sidebar()
nav.run()
