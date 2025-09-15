import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from typing import Optional, Tuple, Dict
from utils.timestamp_utils import timestamp
from settings import (
    LOGIN_PAGE_URL,
    LOGIN_POST_URL,
    MAX_ATTEMPTS_PER_SESSION,
    HEADERS,
    CSRF_PARAM_STRING,
    red_bold,
    reset_text
)


def create_session() -> Optional[requests.Session]:
    """
    Create a requests.Session with default headers and fetch initial cookies.

    Returns:
        Optional[requests.Session]: Configured session if reachable, else None.
    """
    session = requests.Session()
    session.headers.update(HEADERS)
    try:
        resp = session.get(LOGIN_PAGE_URL, timeout=10)
        if resp.status_code != 200:
            print(f"{timestamp()} {red_bold}[!] Server returned status: {resp.status_code}{reset_text}")
            return None
        session.cookies.update(resp.cookies)
        print(f"{timestamp()} [*] Session created and initial cookies fetched.")
    except requests.RequestException as e:
        print(f"{timestamp()} {red_bold}[!] Connection error: {e}{reset_text}")
        return None
    return session


def refresh_session(
    session: requests.Session, counter: int
) -> Tuple[Optional[requests.Session], int]:
    """
    Refresh the session if the attempt counter exceeds the maximum allowed attempts.

    This function checks if the current attempt counter has reached the configured
    maximum attempts per session. If so, it creates a new session and resets the counter.

    Args:
        session (requests.Session): The current HTTP session.
        counter (int): The current number of login attempts with this session.

    Returns:
        Tuple[Optional[requests.Session], int]:
            A tuple containing:
                - The refreshed session (or None if session creation failed).
                - The updated attempt counter (0 if refreshed, unchanged otherwise).
    """
    if counter >= MAX_ATTEMPTS_PER_SESSION:
        print(f"\n{timestamp()} [*] Refreshing session...")
        new_sess = create_session()
        return (new_sess, 0) if new_sess else (None, 0)

    return session, counter


def fetch_login_form(session: requests.Session) -> Tuple[str, Dict[str, str]]:
    """
    Fetch login page and extract form action and input values.

    Args:
        session (requests.Session): Active HTTP session.

    Returns:
        Tuple[str, Dict[str, str]]: (post_url, form_values)
    """
    resp = session.get(LOGIN_PAGE_URL, timeout=10)
    soup = BeautifulSoup(resp.text, "html.parser")
    form = soup.find("form")
    post_url = (
        urljoin(LOGIN_PAGE_URL, form.get("action"))
        if form and form.get("action")
        else LOGIN_POST_URL
    )
    form_values = (
        {
            inp.get("name"): inp.get("value", "")
            for inp in form.find_all("input")
            if inp.get("name")
        }
        if form
        else {}
    )
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
