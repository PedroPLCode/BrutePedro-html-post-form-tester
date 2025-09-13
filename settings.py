"""
Module Constants

This module defines the constants used by the brute-force login script.

Attributes:
    LOGIN_PAGE (str): URL of the login page where CSRF token is fetched.
    LOGIN_POST (str): URL of the POST endpoint to submit login requests.
    USERNAMES_FILE (str): Path to the file containing username list.
    PASSWORDS_FILE (str): Path to the file containing password list.
    SUCCESS_FILE (str): Path to the file where successful username:password
                        combinations are stored.
    PROGRESS_FILE (str): Path to the file tracking the last attempted combination
                         to allow resuming the brute-force attack.
"""

LOGIN_PAGE = "https://login_page_url_here"
LOGIN_POST = "https://login_post_url_here"
USERNAMES_FILE_PATH = "data/usernames.txt"
PASSWORDS_FILE_PATH = "data/passwords.txt"
SUCCESS_FILE_PATH = "data/success.brute"
PROGRESS_FILE_PATH = "data/progress.brute"