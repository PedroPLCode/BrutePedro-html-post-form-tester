import os
from typing import Union, List, Set


def load_file(filepath: str, as_set: bool = False) -> Union[List[str], Set[str]]:
    """
    Loads a file into a list or set (unique lines).

    Args:
        filepath (str): Path to the file to be loaded.
        as_set (bool, optional): If True, returns a set (unique lines),
                                 otherwise returns a list. Defaults to False.

    Returns:
        Union[List[str], Set[str]]: List or set of lines read from the file.
    """
    try:
        if os.path.exists(filepath):
            with open(filepath, "r") as f:
                data = [line.strip() for line in f if line.strip()]
            print(f"[*] Loaded {len(data)} records from {filepath}")
            return set(data) if as_set else data
        print(f"[*] File {filepath} does not exist, creating empty structure.")
        return set() if as_set else []
    except Exception as e:
        print(f"[!] Error reading file {filepath}: {e}")
        return set() if as_set else []


def save_to_file(filepath: str, combo: str) -> None:
    """
    Appends a single line to a file.

    Args:
        filepath (str): Path to the file where the line will be appended.
        combo (str): The line/combination to be written to the file.
    """
    try:
        with open(filepath, "a") as f:
            f.write(f"{combo}\n")
    except Exception as e:
        print(f"[!] Error writing to file {filepath}: {e}")
