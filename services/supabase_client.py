import os

from dotenv import load_dotenv


load_dotenv()


def get_secret(name):
    value = os.getenv(name)
    if value:
        return value

    try:
        import streamlit as st

        secret_value = st.secrets.get(name)
        if secret_value:
            return secret_value
    except Exception:
        pass

    return None


def is_supabase_enabled():
    return bool(get_secret("SUPABASE_URL") and get_secret("SUPABASE_KEY"))


def get_supabase_client():
    if not is_supabase_enabled():
        return None

    from supabase import create_client

    return create_client(
        get_secret("SUPABASE_URL"),
        get_secret("SUPABASE_KEY"),
    )
