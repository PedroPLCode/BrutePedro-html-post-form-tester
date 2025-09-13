import os
import tempfile
from utils.files_utils import load_file, save_to_file


def test_load_file_list_and_set():
    """
    Test loading a file as a list and as a set.

    This test creates a temporary file with duplicate lines and checks:
        - Loading as a list preserves all lines including duplicates.
        - Loading as a set removes duplicates.
    """
    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as tmp:
        tmp.write("line1\nline2\nline3\nline1\n")
        tmp_path = tmp.name

    data_list = load_file(tmp_path, as_set=False)
    assert isinstance(data_list, list)
    assert data_list == ["line1", "line2", "line3", "line1"]

    data_set = load_file(tmp_path, as_set=True)
    assert isinstance(data_set, set)
    assert data_set == {"line1", "line2", "line3"}

    os.remove(tmp_path)


def test_load_file_nonexistent():
    """
    Test loading a non-existent file.

    Checks that loading a file that does not exist returns:
        - An empty list if as_set=False
        - An empty set if as_set=True
    """
    data_list = load_file("nonexistent_file.txt", as_set=False)
    assert data_list == []

    data_set = load_file("nonexistent_file.txt", as_set=True)
    assert data_set == set()


def test_save_to_file_and_load():
    """
    Test saving lines to a file and reloading them.

    Creates a temporary file, saves multiple lines, and ensures
    that load_file reads them back in the correct order.
    """
    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as tmp:
        tmp_path = tmp.name

    save_to_file(tmp_path, "combo1")
    save_to_file(tmp_path, "combo2")

    data = load_file(tmp_path)
    assert data == ["combo1", "combo2"]

    os.remove(tmp_path)
