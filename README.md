# SafeStep — Scam Awareness & Digital Safety App

A multilingual scam-awareness and digital-safety learning app for older adults and first-time smartphone users, available in **English, हिंदी and मराठी**.
Pure Python. Deploys free on **Streamlit Community Cloud** with no server setup.

## GitHub repository

To publish this project, create a repository on GitHub and upload the **contents of this `SafeStep` folder** (including `app.py`, `safestep/`, `data/`, `games/`, `tests/`, and `.streamlit/`). Do not upload a real `.streamlit/secrets.toml` file; keep API keys and credentials private.

## Deploy in 5 minutes (Streamlit Community Cloud)

1. Create a GitHub repository and upload everything in this folder (keep the structure, including `.streamlit/config.toml`).
2. Go to **share.streamlit.io**, sign in with GitHub, and click **Create app → Deploy a public app from GitHub**.
3. Pick your repository, branch `main`, and main file **`app.py`**. Choose a short app URL, for example `safestep-mpstme`.
4. *(Optional, for real SMS and the AI)* open **Advanced settings → Secrets** and paste your settings (see the next section). You can also add them later in the app's **Settings → Secrets**.
5. Click **Deploy**. Your app is live at `https://<your-name>.streamlit.app`.

Without any secrets the app runs in **demo mode**: any 6 digits sign in, and the assistant uses built-in answers. That is ideal for presenting the design.

## Secrets (real OTP and AI)

Paste into the Secrets box. For local runs, copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml`.

```toml
# Sign-in codes: demo | console | twilio | msg91
OTP_PROVIDER = "console"
SHOW_CODE_ON_SCREEN = true        # console mode only: also show the code on screen (classroom demos)

# Twilio Verify (real SMS)
TWILIO_ACCOUNT_SID = "AC..."
TWILIO_AUTH_TOKEN = "..."
TWILIO_VERIFY_SERVICE_SID = "VA..."

# MSG91 (Indian provider, DLT templates)
MSG91_AUTH_KEY = "..."
MSG91_TEMPLATE_ID = "..."

# AI assistant (Claude) — https://console.anthropic.com
ANTHROPIC_API_KEY = "sk-ant-..."
ANTHROPIC_MODEL = "claude-haiku-5-5"
```

| `OTP_PROVIDER` | What happens |
|---|---|
| `demo` (default) | no SMS; any 6 digits sign in |
| `console` | a real random code, printed in **Manage app → Logs**. Add `SHOW_CODE_ON_SCREEN = true` to show it on screen as well |
| `twilio` | Twilio Verify texts and checks the code. A trial account only texts numbers you've verified in the Twilio console |
| `msg91` | MSG91 texts and checks the code. Check the details against MSG91's current API docs |

> In India, business SMS must use a TRAI DLT-registered sender ID and template. Indian providers such as MSG91 help with this. Confirm with your provider before going live.

**Built-in protection:**
- One code per number every 30 seconds, and at most 5 codes per number per hour.
- At most 6 checks per 10 minutes.
- Codes expire after 10 minutes and work only once.

**AI assistant:** with `ANTHROPIC_API_KEY` set, Claude runs as an agent with tools. It can scan a message for scam signs, look up a SafeStep word, and fetch the 1930 / cybercrime.gov.in help steps. It finishes with a structured answer that the app shows with a risk meter, a next step, a "Get help now" button and a link to the word card.
- It always answers in the chosen language, never asks for OTPs or PINs, and allows 40 messages per hour per visitor.
- If the AI can't be reached, the built-in answers take over.

## Run on your computer

```bash
python -m venv .venv && source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```
Open http://localhost:8501.

**Tests:** `pip install pytest`, then `pytest -q`. They click through every page in all three languages, sign in with a real console code, complete a scenario and a 5-question quiz, and run the AI agent against a stand-in Claude API.

## What's where

```
app.py                     pages, navigation, login — every text is t("English", "हिंदी", "मराठी")
safestep/styles.py         colours, fonts, animations (CSS)
safestep/content.py        facts, tips, examples
data/content.json          the 8 scam words with 40 quiz questions, and the 7 scenarios (EN/HI/MR)
games/mini-games.html      the 3 mini games (Message Drop Tower, Build Your Safe Phone, Safe Match), shown on the "Mini Games" page
safestep/checker.py        "Ask Before You Click" warning-sign rules
safestep/otp.py            sign-in codes (demo / console / Twilio / MSG91)
safestep/assistant.py      AI agent + built-in answers
.streamlit/config.toml     theme (teal / cream)
tests/test_app.py          automated tests
```

## Notes
- **Saved progress:** progress lasts for the browser session, because Streamlit keeps state per visit. Add a database such as Supabase or Firestore if you need it saved permanently.
- **Navigation:**
  - Each page has its own web address (`/learn`, `/recap`…), so the browser Back button works.
  - On phones the menu closes by itself after you pick a page, using a tiny script the app adds.
- **Animations:** page entrances, card hovers, the risk meter, highlighted risky words, the goal ring, medals, word cards, typing-in demo SMS, balloons for badges and toasts. All motion is switched off for people who have turned on reduced motion on their device.
- **Not in this version:** voice input and read-aloud, because the Streamlit version has no browser speech features.
