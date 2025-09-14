"""
Module Constants

This module defines the constants used by the brute-force login script.

Attributes:
    LOGIN_PAGE_URL (str): URL of the login page where CSRF token is fetched.
    LOGIN_POST_URL (str): URL of the POST endpoint to submit login requests.
    DEFAULT_SESSION_HEADERS (dict): Default headers for the HTTP session.
    DATA_DIR (str): Directory where data files are stored.
    USERNAMES_FILE (str): Path to the file containing username list.
    PASSWORDS_FILE (str): Path to the file containing password list.
    SUCCESS_FILE (str): Path to the file where successful username:password
                        combinations are stored.
    PROGRESS_FILE (str): Path to the file tracking the last attempted combination
                         to allow resuming the brute-force attack.
    USERNAME_PARAM_STRING (str): The form parameter name for the username field in the login form.
    PASSWORD_PARAM_STRING (str): The form parameter name for the password field in the login form.
    CSRF_PARAM_STRING (str): The form parameter name for the CSRF token field in the login form.
    DELAY_BETWEEN_REQUESTS (float): Delay in seconds between login attempts to avoid rate limiting.
"""

LOGIN_PAGE_URL = "https://example.com/apps/tncms/login.cms"
LOGIN_POST_URL = "https://example.com/login.cms"
DEFAULT_SESSION_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "X-Requested-With": "XMLHttpRequest",
}

DATA_DIR = "data"
USERNAMES_FILE_PATH = f"{DATA_DIR}/usernames.txt"
PASSWORDS_FILE_PATH = f"{DATA_DIR}/passwords_pl.txt"
SUCCESS_FILE_PATH = f"{DATA_DIR}/success.brute"
PROGRESS_FILE_PATH = f"{DATA_DIR}/progress.brute"

USERNAME_PARAM_STRING = "username"
PASSWORD_PARAM_STRING = "password"
CSRF_PARAM_STRING = "csrf_token"

DELAY_BETWEEN_REQUESTS = 1.5
