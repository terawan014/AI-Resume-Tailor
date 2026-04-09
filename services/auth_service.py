from services.supabase_client import get_supabase_client, is_supabase_enabled


def _extract_session(response):
    return getattr(response, "session", None) or getattr(getattr(response, "data", None), "session", None)


def _extract_user(response):
    return getattr(response, "user", None) or getattr(getattr(response, "data", None), "user", None)


def sign_up(email, password):
    client = get_supabase_client()
    response = client.auth.sign_up({"email": email, "password": password})
    return {
        "session": _extract_session(response),
        "user": _extract_user(response),
    }


def sign_in(email, password):
    client = get_supabase_client()
    response = client.auth.sign_in_with_password({"email": email, "password": password})
    return {
        "session": _extract_session(response),
        "user": _extract_user(response),
    }


def restore_user(access_token, refresh_token):
    client = get_supabase_client()
    client.auth.set_session(access_token, refresh_token)
    response = client.auth.get_user()
    return _extract_user(response)


def sign_out(access_token=None, refresh_token=None):
    if not is_supabase_enabled():
        return

    if access_token and refresh_token:
        client = get_supabase_client()
        client.auth.set_session(access_token, refresh_token)
        client.auth.sign_out()
