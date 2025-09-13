import os

def load_file(filepath, as_set=False):
    """Wczytanie pliku do listy lub zestawu (unikalne linie)."""
    try:
        if os.path.exists(filepath):
            with open(filepath, "r") as f:
                data = [line.strip() for line in f if line.strip()]
            print(f"[*] Wczytano {len(data)} rekordów z {filepath}")
            return set(data) if as_set else data
        print(f"[*] Plik {filepath} nie istnieje, tworzymy pustą strukturę.")
        return set() if as_set else []
    except Exception as e:
        print(f"[!] Błąd wczytywania pliku {filepath}: {e}")
        return set() if as_set else []

def save_to_file(filepath, combo):
    """Zapisanie jednej linii do pliku (append)."""
    try:
        with open(filepath, "a") as f:
            f.write(f"{combo}\n")
    except Exception as e:
        print(f"[!] Błąd zapisu do pliku {filepath}: {e}")
