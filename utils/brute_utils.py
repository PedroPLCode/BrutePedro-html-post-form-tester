import time
import requests
from typing import Optional, Set
from bs4 import BeautifulSoup
from settings import LOGIN_PAGE, LOGIN_POST, SUCCESS_FILE_PATH
from utils.files_utils import save_to_file


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
    """
    Attempts to log in using a username, password, and optional CSRF token.

    Args:
        session (requests.Session): Active HTTP session.
        known_success (Set[str]): Set of already successful username:password combinations.
        username (str): The username to try.
        password (str): The password to try.

    Returns:
        bool: True if login was successful, False otherwise.
    """
    data = {"login": username, "password": password}
    csrf_token = get_csrf_token(session)
    if csrf_token:
        data["csrf_token"] = csrf_token

    try:
        start = time.time()
        resp = session.post(LOGIN_POST, data=data)
        time.sleep(1 + (time.time() - start) * 0.5)

        if resp.json().get("error") == False:
            combo = f"{username}:{password}"
            if combo not in known_success:
                save_to_file(SUCCESS_FILE_PATH, combo)
                known_success.add(combo)
            print(f"[+] Success: {combo}")
            return True
        print(f"[-] Failed: {username}:{password}")
    except Exception as e:
        print(f"[!] Response error: {e}")
    return False
