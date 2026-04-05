import os

from dotenv import load_dotenv
from groq import Groq


load_dotenv()


def get_api_key():
    api_key = os.getenv("GROQ_API_KEY")
    if api_key:
        return api_key

    try:
        import streamlit as st

        secret_value = st.secrets.get("GROQ_API_KEY")
        if secret_value:
            return secret_value
    except Exception:
        pass

    return None


def get_client():
    api_key = get_api_key()
    if not api_key:
        raise ValueError(
            "Missing GROQ_API_KEY. Add it to your local .env file or your deployed app secrets."
        )
    return Groq(api_key=api_key)
