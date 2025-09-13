import os
from settings import LOGIN_FILE, PASSWORD_FILE, SUCCESS_FILE, PROGRESS_FILE

def check_and_load_known_success():
    """Wczytanie już znalezionych sukcesów z pliku."""
        # Wczytanie już znalezionych sukcesów
    if os.path.exists(SUCCESS_FILE):
        with open(SUCCESS_FILE, "r") as f:
            known_success = set(line.strip() for line in f)
        print(f"[*] Wczytano {len(known_success)} znanych sukcesów.")
    else:
        known_success = set()
        print("[*] Brak znanych sukcesów.")
    return known_success

def check_and_load_progress():
    """Wczytanie miejsca wznowienia z pliku."""
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r") as f:
            last_combo = f.read().strip()
        print(f"[*] Wznowienie od: {last_combo}")
    else:
        last_combo = None
        print("[*] Brak pliku postępu, zaczynam od początku.")
    return last_combo
    
def load_usernames_and_passwords():
    """Wczytanie loginów i haseł z plików."""
    with open(LOGIN_FILE, "r") as f:
        logins = [line.strip() for line in f if line.strip()]

    with open(PASSWORD_FILE, "r") as f:
        passwords = [line.strip() for line in f if line.strip()]
    
    return logins, passwords

def save_to_file(FILE, combo):
    """Zapisanie sukcesu do pliku."""
    with open(FILE, "a") as f:
        f.write(combo + "\n")