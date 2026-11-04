"""SMS sign-in codes (OTP).

OTP_PROVIDER in secrets:
  demo     – no SMS; any 6 digits sign in (default, good for showing the design)
  console  – a real random code is generated and printed in the app logs (Manage app ▸ Logs on Streamlit Cloud);
             set SHOW_CODE_ON_SCREEN = true to also show it on screen for classroom demos
  twilio   – Twilio Verify sends and checks the code
  msg91    – MSG91 (Indian provider, DLT templates) sends and checks the code
"""
import hashlib
import re
import secrets
import threading
import time

import requests
import streamlit as st

from .config import cfg, cfg_bool

PHONE_RE = re.compile(r"^[6-9]\d{9}$")
CODE_RE = re.compile(r"^\d{6}$")


def provider() -> str:
    p = cfg("OTP_PROVIDER", "demo").strip().lower() or "demo"
    return p if p in ("demo", "console", "twilio", "msg91") else "demo"


def show_code_on_screen() -> bool:
    return provider() == "console" and cfg_bool("SHOW_CODE_ON_SCREEN")


@st.cache_resource
def _store():
    """Shared by every visitor of this app process: console codes and rate-limit counters."""
    return {"lock": threading.Lock(), "codes": {}, "buckets": {}}


def _limited(key: str, max_hits: int, window_s: float) -> bool:
    s = _store()
    now = time.time()
    with s["lock"]:
        n, reset = s["buckets"].get(key, (0, now + window_s))
        if now > reset:
            n, reset = 0, now + window_s
        n += 1
        s["buckets"][key] = (n, reset)
        return n > max_hits


def _sha(x: str) -> str:
    return hashlib.sha256(x.encode()).hexdigest()


def send_code(phone: str, lang: str = "en"):
    """Returns (ok, error, dev_code). error is one of invalid_phone, rate_limited, send_failed."""
    if not PHONE_RE.match(phone or ""):
        return False, "invalid_phone", None
    p = provider()
    if p == "demo":
        return True, None, None
    if _limited("send30:" + phone, 1, 30) or _limited("sendH:" + phone, 5, 3600):
        return False, "rate_limited", None
    try:
        if p == "console":
            code = f"{secrets.randbelow(10**6):06d}"
            with _store()["lock"]:
                _store()["codes"][phone] = {"hash": _sha(code), "exp": time.time() + 600, "tries": 0}
            print(f"[SafeStep OTP] +91 {phone[:5]} {phone[5:]}  →  {code}", flush=True)
            return True, None, code if show_code_on_screen() else None
        if p == "twilio":
            base = cfg("TWILIO_VERIFY_BASE", "https://verify.twilio.com").rstrip("/")
            data = {"To": "+91" + phone, "Channel": "sms"}
            if lang == "hi":
                data["Locale"] = "hi"
            r = requests.post(f"{base}/v2/Services/{cfg('TWILIO_VERIFY_SERVICE_SID')}/Verifications", data=data,
                              auth=(cfg("TWILIO_ACCOUNT_SID"), cfg("TWILIO_AUTH_TOKEN")), timeout=20)
            if r.status_code == 429:
                return False, "rate_limited", None
            ok = r.status_code < 300 and r.json().get("status") == "pending"
            if not ok:
                print("[twilio send]", r.status_code, r.text[:300], flush=True)
            return ok, None if ok else "send_failed", None
        if p == "msg91":
            base = cfg("MSG91_BASE", "https://control.msg91.com").rstrip("/")
            r = requests.post(f"{base}/api/v5/otp", params={"template_id": cfg("MSG91_TEMPLATE_ID"), "mobile": "91" + phone,
                              "otp_length": "6", "otp_expiry": "10"}, headers={"authkey": cfg("MSG91_AUTH_KEY")}, json={}, timeout=20)
            ok = r.ok and r.json().get("type") == "success"
            if not ok:
                print("[msg91 send]", r.status_code, r.text[:300], flush=True)
            return ok, None if ok else "send_failed", None
    except Exception as e:  # network problems, bad JSON…
        print("[otp send]", repr(e), flush=True)
    return False, "send_failed", None


def check_code(phone: str, code: str):
    """Returns (ok, error). error is one of wrong_code, expired, rate_limited, send_failed."""
    if not CODE_RE.match(code or "") or not PHONE_RE.match(phone or ""):
        return False, "wrong_code"
    p = provider()
    if p == "demo":
        return True, None
    if _limited("verify:" + phone, 6, 600):
        return False, "rate_limited"
    try:
        if p == "console":
            with _store()["lock"]:
                e = _store()["codes"].get(phone)
                if not e or e["exp"] < time.time():
                    return False, "expired"
                e["tries"] += 1
                if e["tries"] > 5:
                    _store()["codes"].pop(phone, None)
                    return False, "expired"
                if e["hash"] != _sha(code):
                    return False, "wrong_code"
                _store()["codes"].pop(phone, None)
                return True, None
        if p == "twilio":
            base = cfg("TWILIO_VERIFY_BASE", "https://verify.twilio.com").rstrip("/")
            r = requests.post(f"{base}/v2/Services/{cfg('TWILIO_VERIFY_SERVICE_SID')}/VerificationCheck",
                              data={"To": "+91" + phone, "Code": code}, auth=(cfg("TWILIO_ACCOUNT_SID"), cfg("TWILIO_AUTH_TOKEN")), timeout=20)
            if r.status_code == 404:
                return False, "expired"
            if r.status_code == 429:
                return False, "rate_limited"
            return (True, None) if r.json().get("status") == "approved" else (False, "wrong_code")
        if p == "msg91":
            base = cfg("MSG91_BASE", "https://control.msg91.com").rstrip("/")
            r = requests.get(f"{base}/api/v5/otp/verify", params={"otp": code, "mobile": "91" + phone},
                             headers={"authkey": cfg("MSG91_AUTH_KEY")}, timeout=20)
            j = r.json()
            if j.get("type") == "success":
                return True, None
            return False, "expired" if "expire" in str(j.get("message", "")).lower() else "wrong_code"
    except Exception as e:
        print("[otp check]", repr(e), flush=True)
    return False, "send_failed"
