in progress

to do:
-poprawki
-refactor
-black
-write nice readme :)



HTML POST Form Brute-Force Tool
Project Overview

This Python project is a brute-force tool for HTML POST login forms that handle CSRF tokens. It can:

Attempt login using username and password lists.

Handle dynamic CSRF tokens for each login request.

Resume from the last attempted combination in case of interruption.

Store successful login combinations in a file.

Save progress to allow continuation without repeating previous attempts.

Log attempts and handle basic network errors gracefully.

Important: This tool is intended for authorized testing only. Using it without explicit permission is illegal.




Features

CSRF token support: Automatically retrieves the CSRF token from the login page before each attempt.

Resume support: Stores progress in a file, allowing you to resume from the last attempted combination.

Success tracking: Stores successful username:password combinations to avoid repeated attempts.

Configurable input files: Supports separate username and password files.

Dynamic timing: Adds a delay based on request response time to reduce server load.



Requirements

Python 3.10+
we havw requirements.txt


Settings conf :
LOGIN_PAGE – URL of the login page where CSRF is obtained.

LOGIN_POST – URL of the POST request for login.

USERNAMES_FILE – File containing usernames, one per line.

PASSWORDS_FILE – File containing passwords, one per line.

PROGRESS_FILE – File where progress is saved.

SUCCESS_FILE – File where successful credentials are saved.


Usage

Run the brute-force script:
python3 main.py

Tests




The script will:

Load previously successful combinations (success.txt) to avoid repeats.

Load progress (progress.txt) to resume unfinished attempts.

Attempt login for each username:password combination.

Save successful attempts to success.txt.

Save each attempted combination to progress.txt for resuming.

KeyboardInterrupt Handling: Press CTRL+C to stop the script safely; the current progress will be saved automatically.




Security and Legal Notice

This tool is intended for penetration testing on systems you own or have permission to test.

Unauthorized use against other systems is illegal and may result in criminal or civil penalties.

Always test responsibly and with permission.