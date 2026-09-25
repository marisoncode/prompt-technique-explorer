"""
Central place for configuration. Nothing else in the project should
call os.getenv() directly — everything reads from here instead.
This is the pattern real projects use so that config only has ONE
place it can go wrong, instead of being scattered across files.
"""

import os
from dotenv import load_dotenv

load_dotenv()


def _get_setting(key: str, default: str = "") -> str:
    """Check Streamlit's secrets store first (used when deployed on
    Streamlit Cloud), fall back to a normal environment variable
    (used when running locally via .env). Wrapped in try/except because
    st.secrets throws an error — not just returns None — when no
    secrets file exists at all, which is the normal case locally."""
    try:
        import streamlit as st
        if key in st.secrets:
            return st.secrets[key]
    except Exception:
        pass
    return os.getenv(key, default)


class Config:
    GEMINI_API_KEY: str = _get_setting("GEMINI_API_KEY")
    GEMINI_MODEL: str = _get_setting("GEMINI_MODEL", "gemini-3.8-flash")

    @classmethod
    def validate(cls) -> None:
        """Fail fast and loudly if required config is missing, instead of
        letting a confusing error happen later deep inside an API call."""
        if not cls.GEMINI_API_KEY:
            raise ValueError(
                "GEMINI_API_KEY is missing. Add it to your .env file "
                "(see .env.example)."
            )