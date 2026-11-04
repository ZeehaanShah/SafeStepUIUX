"""SafeStep Assistant.

Live mode (ANTHROPIC_API_KEY set): Claude acts as an agent with tools — check_message, lookup_scam_term,
get_help_steps — and finishes with a structured `respond` tool call that the app renders (risk meter, next step…).
Offline mode: built-in rule-based answers, so the page always works.
"""
import json

import requests

from .checker import analyze
from .config import cfg
from .content import TERM, TERMS
from .i18n import L, t

GLOSSARY = {x["key"]: {"name": x["name"][0], "what_it_is": x["d"][0], "example": x["ex"][0],
                       "how_to_stay_safe": x["tip"][0], "remember": x["rem"][0]} for x in TERMS}
HELP_STEPS = {"steps": ["Stop: hang up, do not share any more codes, PINs or money.",
                        "Call your bank on the number printed on your card or in the official app to block the card / UPI and stop payments.",
                        "Report it immediately on the national cyber crime helpline 1930 or at https://cybercrime.gov.in — reporting within the first hours gives the best chance of stopping the money.",
                        "If a remote-access app was installed, uninstall it and change your banking passwords from another phone."],
              "note": "Scams happen to careful people too. Acting quickly was the right thing to do."}
TOOLS = [
    {"name": "check_message", "description": "Scan the text of an SMS, WhatsApp message, email or call description for common Indian scam warning signs. Returns a rough risk level and the signs found. Use it whenever the user shares or describes a message or call.",
     "input_schema": {"type": "object", "properties": {"text": {"type": "string"}}, "required": ["text"]}},
    {"name": "lookup_scam_term", "description": "Get SafeStep's plain-language explanation, example and safety tip for a scam word.",
     "input_schema": {"type": "object", "properties": {"term": {"type": "string", "enum": list(GLOSSARY)}}, "required": ["term"]}},
    {"name": "get_help_steps", "description": "Official steps (India) for someone who may already have lost money or shared an OTP/PIN.",
     "input_schema": {"type": "object", "properties": {}}},
    {"name": "respond", "description": "Send your final answer to the user. Always finish by calling this exactly once.",
     "input_schema": {"type": "object", "properties": {
         "reply": {"type": "string", "description": "Answer in the user's language, plain and warm, at most about 90 words"},
         "risk": {"type": "string", "enum": ["none", "low", "medium", "high"]},
         "next_step": {"type": "string", "description": "One short concrete thing to do now, in the user's language (empty if not needed)"},
         "show_help_button": {"type": "boolean", "description": "True if money or a code may already be gone"},
         "related_term": {"type": "string", "enum": [""] + list(GLOSSARY)}},
         "required": ["reply", "risk", "next_step", "show_help_button", "related_term"]}},
]
LANG_NAME = {"en": "English", "hi": "Hindi (Devanagari script)", "mr": "Marathi (Devanagari script)"}


def ai_enabled() -> bool:
    return bool(cfg("ANTHROPIC_API_KEY"))


def system_prompt(lang: str) -> str:
    return f"""You are the SafeStep Assistant, a kind helper for older adults and first-time smartphone users in India who want to check whether a call, message, link, QR code or payment request is a scam.
Always answer in {LANG_NAME.get(lang, 'English')}, whatever language the question is in, using short sentences, everyday words and no jargon. Be calm and reassuring, never scary or blaming.
Rules:
- Never ask for, and tell the user never to share, OTPs, PINs, passwords, CVV or full card/account numbers. If they paste one, tell them gently not to share it with anyone.
- Use check_message when the user shares or describes a message or call. Use get_help_steps when money or a code may already be gone. Use lookup_scam_term when a SafeStep word would help.
- Give one clear next step. In India the cyber crime helpline is 1930 and the portal is cybercrime.gov.in. Banks, police, couriers and government offices never ask for OTPs or payments over calls, SMS links or video calls; receiving money never needs a UPI PIN.
- You cannot see the user's phone, bank or messages beyond what they type. Do not invent phone numbers or links.
- If the question has nothing to do with staying safe from fraud, answer briefly and kindly steer back.
- Finish every turn by calling the respond tool exactly once."""


def _tool(name: str, args: dict):
    if name == "check_message":
        r = analyze(str(args.get("text", "")))
        return {"risk": {"high": "high", "mid": "medium", "low": "low"}[r["level"]], "score": r["score"],
                "warning_signs": [f["t"][0] for f in r["flags"]]}
    if name == "lookup_scam_term":
        return GLOSSARY.get(args.get("term"), {"error": "unknown term"})
    if name == "get_help_steps":
        return HELP_STEPS
    return {"error": "unknown tool"}


def run_agent(lang: str, history: list) -> dict:
    """history: [{"role": "user"|"assistant", "content": str}] ending with the user's message."""
    base = cfg("ANTHROPIC_BASE_URL", "https://api.anthropic.com").rstrip("/")
    headers = {"x-api-key": cfg("ANTHROPIC_API_KEY"), "anthropic-version": "2023-06-01", "content-type": "application/json"}
    messages = [{"role": m["role"], "content": m["content"][:2000]} for m in history[-12:]]
    while messages and messages[0]["role"] != "user":
        messages.pop(0)
    for _ in range(5):
        r = requests.post(f"{base}/v1/messages", headers=headers, timeout=30, json={
            "model": cfg("ANTHROPIC_MODEL", "claude-haiku-5-5"), "max_tokens": 1024,
            "system": system_prompt(lang), "tools": TOOLS, "messages": messages})
        r.raise_for_status()
        content = r.json().get("content", [])
        final = next((b for b in content if b.get("type") == "tool_use" and b.get("name") == "respond"), None)
        if final:
            out = dict(final.get("input") or {})
            out.setdefault("risk", "none"); out.setdefault("next_step", ""); out.setdefault("show_help_button", False); out.setdefault("related_term", "")
            return out
        uses = [b for b in content if b.get("type") == "tool_use"]
        if not uses:
            text = "\n".join(b.get("text", "") for b in content if b.get("type") == "text").strip()
            return {"reply": text or "…", "risk": "none", "next_step": "", "show_help_button": False, "related_term": ""}
        messages.append({"role": "assistant", "content": content})
        messages.append({"role": "user", "content": [{"type": "tool_result", "tool_use_id": u["id"],
                                                      "content": json.dumps(_tool(u["name"], u.get("input") or {}))} for u in uses]})
    raise RuntimeError("agent: too many tool turns")


def offline_reply(q: str) -> dict:
    """Built-in answers used when no AI key is set or the AI can't be reached."""
    import re
    s = q.lower()
    if re.search(r"otp|call|caller|bank|कॉल|ओटीपी|बैंक|बँक|फोन", q, re.I):
        return {"reply": t("Let’s check. Here’s what I found: an urgent tone, a request for your OTP, and a caller you don’t already know. This is likely a scam call.",
                           "आइए जांचते हैं। मुझे यह मिला: जल्दबाज़ी वाला लहजा, आपका OTP मांगा गया, और कॉलर आपका जाना-पहचाना नहीं है। यह संभवतः ठगी वाली कॉल है।",
                           "चला तपासूया. मला हे आढळले: घाईचा सूर, तुमचा OTP मागितला, आणि कॉलर तुमच्या ओळखीचा नाही. हा बहुधा फसवणुकीचा कॉल आहे."),
                "risk": "high", "next_step": t("Don’t share the OTP. Hang up and call your bank on the number on your card.",
                                               "OTP न बताएं। फोन काटें और कार्ड पर लिखे नंबर पर बैंक को कॉल करें।",
                                               "OTP सांगू नका. फोन ठेवा आणि कार्डवरील नंबरवर बँकेला कॉल करा."),
                "show_help_button": True, "related_term": "OTP Fraud"}
    if re.search(r"vishing|विशिंग|व्हिशिंग", q, re.I):
        x = TERM["Vishing"]
        return {"reply": f"{L(x['name'])}: {L(x['d'])}", "risk": "none", "next_step": L(x["tip"]), "show_help_button": False, "related_term": "Vishing"}
    if re.search(r"qr|scan|स्कैन|स्कॅन", q, re.I):
        x = TERM["QR Code Scam"]
        return {"reply": t("Before you scan or pay, check two things: the shop name on YOUR screen matches the shop, and you never enter a PIN to receive money.",
                           "स्कैन या भुगतान से पहले दो बातें जांचें: आपकी स्क्रीन पर दिखा नाम दुकान से मेल खाता है, और पैसा पाने के लिए कभी पिन न डालें।",
                           "स्कॅन किंवा पैसे देण्यापूर्वी दोन गोष्टी तपासा: तुमच्या स्क्रीनवर दिसणारे नाव दुकानाशी जुळते, आणि पैसे मिळवण्यासाठी कधीही पिन टाकू नका."),
                "risk": "none", "next_step": L(x["rem"]), "show_help_button": False, "related_term": "QR Code Scam"}
    r = analyze(q)
    if r["flags"]:
        return {"reply": t("Here’s how that reads to me: ", "मुझे यह ऐसा लगता है: ", "मला हे असे वाटते: ") + "; ".join(L(f["t"]) for f in r["flags"]) + ".",
                "risk": {"high": "high", "mid": "medium", "low": "low"}[r["level"]],
                "next_step": t("When in doubt, pause and check through an official app or number you already trust.",
                               "शक हो तो रुकें और पहले से भरोसेमंद ऐप या नंबर से जांचें।",
                               "शंका असल्यास थांबा आणि आधीपासून विश्वासाच्या ॲप किंवा नंबरवरून खात्री करा."),
                "show_help_button": False, "related_term": ""}
    return {"reply": t("I can help with calls, messages, links and payments. Try telling me what the message said or what the caller asked for.",
                       "मैं कॉल, संदेश, लिंक और भुगतान में मदद कर सकता हूं। बताइए संदेश में क्या लिखा था या कॉलर ने क्या मांगा।",
                       "मी कॉल, संदेश, लिंक आणि पेमेंटबद्दल मदत करू शकतो. संदेशात काय लिहिले होते किंवा कॉलरने काय मागितले ते सांगा."),
            "risk": "none", "next_step": "", "show_help_button": False, "related_term": ""}
