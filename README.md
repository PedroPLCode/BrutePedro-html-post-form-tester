# BrutePedro — HTML POST form tester
BrutePedro is a small Python tool for testing HTML POST login forms that use CSRF tokens / AJAX.
It is designed for authorized penetration testing only and includes resumable bruteforce logic, CSRF handling, and unit tests that run without hitting the network (they use mocks).
<br>Current version: 1.0

### Note
This script was developed for a concrete test I performed and is focused on that task. You’re encouraged to adapt and extend it to meet your own requirements. Suggestions, comments and feedback are much appreciated!

### Features
- Fetches dynamic CSRF token from the login page before each POST attempt.
- Maintains a requests Session (cookies preserved between requests).
- Resumable: the script saves progress and can resume where it left off.
- Records successful username:password pairs to a file.
- Configurable delay between requests to reduce server load.
- Unit tests with pytest and unittest.mock — no real network needed for tests.

### WARNING / Legal / Ethics
You must have explicit permission from the owner of the target system before running attacks or brute-force tests. Unauthorized testing is illegal and unethical. Use this tool only on systems you own or where you have written authorization.

### Requirements
- Python 3.8+ (3.10+ recommended)
- Dependencies listed in requirements.txt

### Installation
```bash
git clone https://github.com/PedroPLCode/BrutePedro-html-post-form-tester.git
cd BrutePedro-html-post-form-tester
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Preparaion
Edit settings.py to point to the target and data directory
```bash
LOGIN_PAGE_URL = "https://example.com/apps/login"
LOGIN_POST_URL = "https://example.com/login"
HEADERS = {
    "default_session_headers"
}
DELAY_BETWEEN_REQUESTS = in seconds
MAX_ATTEMPTS_PER_SESSION = int

DATA_DIR = "data"
USERNAMES_FILE_PATH = f"{DATA_DIR}/usernames.txt"
PASSWORDS_FILE_PATH = f"{DATA_DIR}/passwords.txt"
SUCCESS_FILE_PATH = f"{DATA_DIR}/success.brute"
PROGRESS_FILE_PATH = f"{DATA_DIR}/progress.brute"

USERNAME_PARAM_STRING = "username"
PASSWORD_PARAM_STRING = "password"
CSRF_PARAM_STRING = "csrf_token"
WRONG_CREDENTIALS_MESSAGE = "Login or password invalid"

```
Place your usernames.txt and passwords.txt files into the data/ folder (or change the paths accordingly).

### Usage
```bash
python run.py
```
Press CTRL+C to stop — the script will save the current progress to data/progress.brute and exit.

### Testing
Run tests from project root so Python finds the utils package:
```bash
pytest -v
```
Tests use mocks to simulate HTTP responses (CSRF token, POST responses). They do not perform real network calls.
If pytest says ModuleNotFoundError: No module named 'utils', run it from the repository root or set PYTHONPATH:
```bash
PYTHONPATH=$(pwd) pytest -v
```

### Troubleshooting
- ModuleNotFoundError: No module named 'bs4' → pip install beautifulsoup4.
- If your endpoint returns HTML (not JSON), resp.json() will raise — modify try_login() to parse HTML or adjust success/failure detection.
- If script connects to 127.0.0.1 unexpectedly — check settings.py for correct LOGIN_PAGE/LOGIN_POST (use https:// if appropriate).

### Use responsibly and only against systems you own or have explicit permission to test
This tool is intended solely for ethical testing purposes. Unauthorized use against systems you do not own or do not have explicit permission to test is illegal and unethical. Always ensure you have proper authorization before conducting any brute force or penetration testing activities. Misuse of this software can lead to serious legal consequences. Use it responsibly, respecting privacy and security policies.

Familiarize yourself thoroughly with the source code. Understand its operation. Only then will you be able to customize and adjust scripts to your own needs, preferences, and requirements. Only then will you be able to use it correctly and avoid potential issues. Knowledge of the underlying code is essential for making informed decisions and ensuring the successful implementation of this script for your specific use case. Make sure to review all components and dependencies before running the scripts.

This project is licensed under GNU General Public License Version 3, 29 June 2007