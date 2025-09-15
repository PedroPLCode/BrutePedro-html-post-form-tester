from typing import Optional
from utils.brute_utils import try_login
from utils.session_utils import create_session
from utils.files_utils import load_file, save_to_file
from utils.info_utils import create_results_summary, timestamp
from settings import (
    USERNAMES_FILE_PATH,
    PASSWORDS_FILE_PATH,
    SUCCESS_FILE_PATH,
    PROGRESS_FILE_PATH,
    bold_text,
    green_bold,
    red_bold,
    reset_text
)

_prev_len = 0


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
    global _prev_len

    print(f"{bold_text}BrutePedro - html-post-form brute-force tester v1.0{reset_text}\n"
          f"{timestamp()} [*] Hello world! Preparing brute-force attack...")

    session = create_session()
    if not session:
        print(f"{timestamp()} {red_bold}[!] Failed to create session.{reset_text}")
        return

    known_success = load_file(SUCCESS_FILE_PATH, as_set=True)
    progress_list = load_file(PROGRESS_FILE_PATH)
    last_saved_combo: Optional[str] = progress_list[-1] if progress_list else None
    resume: bool = last_saved_combo is None

    usernames = load_file(USERNAMES_FILE_PATH)
    passwords = load_file(PASSWORDS_FILE_PATH)
    if not usernames or not passwords:
        print(f"{timestamp()} {red_bold}[!] Username or password files are empty.{reset_text}")
        return

    combo: Optional[str] = None
    previous_tested_combo: Optional[str] = None
    attempt_counter = 0
    try:
        for username in usernames:
            for password in passwords:
                combo = f"{username}:{password}"

                if combo in known_success:
                    continue

                if not resume:
                    if combo == last_saved_combo:
                        resume = True
                    continue

                success, attempt_counter = try_login(
                    session, known_success, username, password, attempt_counter
                )
                save_to_file(PROGRESS_FILE_PATH, combo, overwrite=True)
                previous_tested_combo = combo

                padding = " " * max(0, _prev_len - len(combo))
                _prev_len = len(combo)
                if success:
                    print(f"\n{timestamp()} {green_bold}[+] Successful combination found: {combo}{reset_text}"
                          f"\n{timestamp()} {bold_text}[?] It can be a false positive, please verify this credential manually.{reset_text}")
                else:
                    print(f"\r{timestamp()} [-] Failed attempt: {combo}{padding}", end="", flush=True)

    except (KeyboardInterrupt, Exception) as e:
        if isinstance(e, KeyboardInterrupt):
            print(f"\n{timestamp()} {bold_text}[!] Interrupted by user. Saving progress and exiting.{reset_text}")
        else:
            print(f"\n{timestamp()} {red_bold}[!] An unexpected error occurred: {e}. Saving progress and exiting.{reset_text}")
        if combo:
            save_to_file(PROGRESS_FILE_PATH, previous_tested_combo, overwrite=True)
            print(f"{timestamp()} {bold_text}[*] Progress saved in {PROGRESS_FILE_PATH}.{reset_text}")
        summary = create_results_summary(known_success, success)
        print(summary)
        raise SystemExit(1)

    print(f"{timestamp()} {bold_text}[*] Brute-force attack completed.{reset_text}")
    summary = create_results_summary(known_success, success)
    print(summary)


if __name__ == "__main__":
    run_brute_force()
