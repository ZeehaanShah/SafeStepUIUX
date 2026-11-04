"""Three languages: every text is written as t("English", "हिंदी", "मराठी")."""
import streamlit as st

LANGS = {"en": "English", "hi": "हिंदी", "mr": "मराठी"}
LOCALE = {"en": "en-IN", "hi": "hi-IN", "mr": "mr-IN"}
_IDX = {"en": 0, "hi": 1, "mr": 2}


def lang() -> str:
    return st.session_state.get("lang", "en")


def t(en: str, hi: str, mr: str) -> str:
    return {"en": en, "hi": hi, "mr": mr}[lang()]


def L(arr) -> str:
    """Pick the current language from a [en, hi, mr] list (falls back to Hindi, then English)."""
    i = _IDX[lang()]
    return arr[i] if len(arr) > i else arr[min(len(arr) - 1, 1)]
