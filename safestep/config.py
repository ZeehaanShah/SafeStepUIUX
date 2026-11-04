"""Settings come from Streamlit secrets (.streamlit/secrets.toml or the Cloud 'Secrets' box), then environment variables."""
import os

import streamlit as st


def cfg(key: str, default: str = "") -> str:
    try:
        val = st.secrets.get(key)
    except Exception:  # no secrets file at all
        val = None
    if val in (None, ""):
        val = os.environ.get(key, default)
    return str(val) if val is not None else default


def cfg_bool(key: str, default: bool = False) -> bool:
    return cfg(key, "true" if default else "false").strip().lower() in ("1", "true", "yes", "on")
