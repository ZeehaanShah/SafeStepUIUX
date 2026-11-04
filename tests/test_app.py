"""Run with:  pytest -q     (needs: pip install pytest)
Uses Streamlit's AppTest to click through the real app without a browser."""
import os
import sys
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
os.chdir(ROOT)

from safestep import checker, otp  # noqa: E402

PAGES = ["home", "ask", "learn", "practice", "games", "scenario", "recap", "assistant", "help", "account"]


def new_app(**env) -> AppTest:
    for k in ("OTP_PROVIDER", "ANTHROPIC_API_KEY", "SHOW_CODE_ON_SCREEN"):
        os.environ.pop(k, None)
    os.environ.update(env)
    at = AppTest.from_file(str(ROOT / "app.py"), default_timeout=30)
    at.run()
    assert not at.exception, at.exception
    return at


def goto(at, page, **state):
    for k, v in state.items():
        at.session_state[k] = v
    at.session_state.goto = page
    at.run()
    assert not at.exception, (page, at.exception)
    assert at.session_state.page == page, (page, at.session_state.page)


def btn(at, key):
    return next(b for b in at.button if b.key == key)


def login(at, code="123456"):
    at.text_input[0].input("9876543210")
    at.button[0].click().run()          # Send Code (form submit)
    assert not at.exception, at.exception
    at.text_input[0].input(code)
    next(b for b in at.button if "Verify" in b.label or "सत्यापित" in b.label or "पडताळणी" in b.label).click().run()
    assert not at.exception, at.exception


def test_demo_login_and_every_page_in_three_languages():
    at = new_app()
    login(at)
    assert at.session_state.authed
    for lg in ("en", "hi", "mr"):
        at.session_state.lang = lg
        for p in PAGES:
            goto(at, p)


def test_wrong_phone_shows_error():
    at = new_app()
    at.text_input[0].input("12345")
    at.button[0].click().run()
    assert at.error and "10-digit" in at.error[0].value


def test_console_otp_real_code_flow():
    at = new_app(OTP_PROVIDER="console", SHOW_CODE_ON_SCREEN="true")
    at.text_input[0].input("9123456780")
    at.button[0].click().run()
    code = at.session_state.dev_code
    assert code and len(code) == 6
    at.text_input[0].input("000000" if code != "000000" else "111111")
    next(b for b in at.button if "Verify" in b.label).click().run()
    assert not at.session_state.authed and at.error
    at.text_input[0].input(code)
    next(b for b in at.button if "Verify" in b.label).click().run()
    assert at.session_state.authed


def test_checker_scenario_and_quiz_flows():
    at = new_app()
    login(at)
    # Ask Before You Click
    goto(at, "ask")
    btn(at, "ex_0").click().run()
    next(b for b in at.button if b.label == "Check it").click().run()
    assert at.session_state.ask_res["level"] == "high"
    # Scenario: wrong answer, reveal, then right answer earns the badge
    goto(at, "scenario", scen_idx=5)
    btn(at, "choice_s5B").click().run()
    assert at.session_state.scen["The Investment Group"]["first"] is False
    next(b for b in at.button if b.label == "See the safer choice").click().run()
    next(b for b in at.button if b.label == "Try this one again").click().run()
    btn(at, "choice_s5A").click().run()
    assert "Smart Saver" in at.session_state.badges
    # Word quiz inside the dialog: answer all five
    goto(at, "learn")
    btn(at, "learn_Vishing").click().run()
    for step in range(1, 6):
        btn(at, f"choice_q{step}A").click().run()
        next(b for b in at.button if b.label in ("Next question", "Finish")).click().run()
        assert not at.exception, at.exception
    assert at.session_state.quiz["Vishing"]["done"] and "Word Wise" in at.session_state.badges


def test_assistant_offline_answer():
    at = new_app()
    login(at)
    goto(at, "assistant")
    at.chat_input[0].set_value("A caller from my bank wants my OTP").run()
    assert not at.exception, at.exception
    last = at.session_state.chat[-1]
    assert last["role"] == "assistant" and last["meta"]["risk"] == "high"


def test_checker_finds_signs_in_all_languages():
    assert checker.analyze("URGENT: share OTP at bit.ly/x")["level"] == "high"
    assert checker.analyze("प्रिय ग्राहक, अभी OTP बताएं")["level"] == "high"
    assert checker.analyze("तातडीने तुमचा पिन सांगा")["level"] == "high"
    assert checker.analyze("Reached office safely, will call later")["level"] == "low"
    html = checker.highlight("Share OTP now", checker.analyze("Share OTP now")["flags"])
    assert "<mark" in html


def test_otp_rejects_bad_numbers():
    assert otp.send_code("12345")[1] == "invalid_phone"
    assert otp.check_code("9876543210", "12")[1] == "wrong_code"


def test_ai_agent_tool_round_trip_with_fake_claude():
    """A fake Claude API asks for check_message, then answers with the respond tool."""
    import json
    import threading
    from http.server import BaseHTTPRequestHandler, HTTPServer

    class Fake(BaseHTTPRequestHandler):
        def do_POST(self):
            body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
            assert self.headers["anthropic-version"] == "2023-06-01" and "Marathi" in body["system"]
            last = body["messages"][-1]
            if isinstance(last["content"], str):
                content = [{"type": "tool_use", "id": "t1", "name": "check_message", "input": {"text": last["content"]}}]
            else:
                risk = json.loads(last["content"][0]["content"])["risk"]
                content = [{"type": "tool_use", "id": "t2", "name": "respond", "input": {"reply": "हा फसवणुकीचा कॉल वाटतो.", "risk": risk,
                            "next_step": "फोन ठेवा.", "show_help_button": True, "related_term": "OTP Fraud"}}]
            out = json.dumps({"type": "message", "role": "assistant", "content": content, "stop_reason": "tool_use"}).encode()
            self.send_response(200); self.send_header("content-type", "application/json"); self.end_headers(); self.wfile.write(out)

        def log_message(self, *a):
            pass

    srv = HTTPServer(("127.0.0.1", 0), Fake)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    try:
        at = new_app(ANTHROPIC_API_KEY="test-key", ANTHROPIC_BASE_URL=f"http://127.0.0.1:{srv.server_port}")
        login(at)
        at.session_state.lang = "mr"
        goto(at, "assistant")
        at.chat_input[0].set_value("बँकेतून फोन आला, तातडीने OTP मागत आहेत").run()
        assert not at.exception, at.exception
        meta = at.session_state.chat[-1]["meta"]
        assert meta["risk"] == "high" and meta["related_term"] == "OTP Fraud" and meta["show_help_button"]
        assert not at.session_state.chat[-1]["note"], "should be a live answer, not the offline fallback"
    finally:
        srv.shutdown()
        os.environ.pop("ANTHROPIC_BASE_URL", None)
