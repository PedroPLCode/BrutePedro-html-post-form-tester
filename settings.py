"""
Module Constants

This module defines the constants used by the brute-force login script.

Attributes:
    LOGIN_PAGE_URL (str): Full URL of the login page where CSRF token is fetched including port to connect.
    LOGIN_POST_URL (str): Full URL of the POST endpoint to submit login requests including port to connect.
    REDIRECT_URL (str): The URL to redirect to after a successful login.
    HEADERS (dict): Default headers for the HTTP session.
    DELAY_BETWEEN_REQUESTS (float): Delay in seconds between login attempts to avoid rate limiting.
    MAX_ATTEMPTS_PER_SESSION (int): Number of login attempts before refreshing the session.
    DUMMY_USERNAME (str): Usermane used only to check server status and response.
    DUMMY_PASSWORD:(str): Password used only to check server status and response.
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
    REDIRECT_PARAM_STRING (str): The form parameter name for the redirect field in the login form.
    ERROR_PARAM_STRING (str): Key in the JSON response indicating an error.
    CLEAR_PARAM_STRING (str): Key in the JSON response indicating a clear status.
    LINK_PARAM_STRING (str): Key in the JSON response indicating a link.
    MESSAGE_PARAM_STRING (str): Key in the JSON response containing a message.
    WRONG_CREDENTIALS_MESSAGE (str): Message indicating wrong credentials in the response.
    SUCCESSFUL_LOGIN_MESSAGE (str): Message indicating a successful login in the response.
    bold_text (str): ANSI escape code for bold text formatting in terminal
    green_bold (str): ANSI escape code for green bold text formatting in terminal
    red_bold (str): ANSI escape code for red bold text formatting in terminal
    reset_text (str): ANSI escape code to reset text formatting in terminal
"""

LOGIN_PAGE_URL: str = "https://example.com/apps/tncms/login.cms"
LOGIN_POST_URL: str = "https://example.com/login.cms"
REDIRECT_URL: str = "/apps/tncms/login.cms"
HEADERS: dict[str, str] = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
    "Accept-Encoding": "gzip, deflate",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Connection": "keep-alive",
    "Referer": LOGIN_PAGE_URL,
    "Origin": f"https://{LOGIN_PAGE_URL.split('://')[1].split('/')[0]}",
    "Accept-Language": "pl,en-US;q=0.7,en;q=0.3",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "X-Requested-With": "XMLHttpRequest",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "Priority": "u=0",
    "Te": "trailers",
}
DELAY_BETWEEN_REQUESTS: float = 1.5
MAX_ATTEMPTS_PER_SESSION: int = 25
DUMMY_USERNAME: str = "dummy_username"
DUMMY_PASSWORD: str = "dummy_password"

DATA_DIR: str = "data"
USERNAMES_FILE_PATH: str = f"{DATA_DIR}/usernames.txt"
PASSWORDS_FILE_PATH: str = f"{DATA_DIR}/passwords.txt"
SUCCESS_FILE_PATH: str = f"{DATA_DIR}/success.brute"
PROGRESS_FILE_PATH: str = f"{DATA_DIR}/progress.brute"

USERNAME_PARAM_STRING: str = "username"
PASSWORD_PARAM_STRING: str = "password"
CSRF_PARAM_STRING: str = "csrf_token"
REDIRECT_PARAM_STRING: str = "redirect"
ERROR_PARAM_STRING: str = "error"
CLEAR_PARAM_STRING: str = "clear"
LINK_PARAM_STRING: str = "link"
MESSAGE_PARAM_STRING: str = "message"
WRONG_CREDENTIALS_MESSAGE: str = "Błędne dane logowania"
SUCCESSFUL_LOGIN_MESSAGE: str = "Logowanie powiodło się"

bold_text: str = "\033[1m"
green_bold: str = "\033[1;32m"
red_bold: str = "\033[1;31m"
reset_text: str = "\033[0m"
