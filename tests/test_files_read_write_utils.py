import os
import tempfile
from utils.files_read_write_utils import load_file, save_to_file


def test_save_to_file_append(tmp_path):
    """Test that lines are appended to a file.

    Args:
        tmp_path (pathlib.Path): Temporary directory provided by pytest.
    """
    file_path = tmp_path / "test.txt"

    save_to_file(file_path, "line1")
    save_to_file(file_path, "line2")

    content = file_path.read_text().splitlines()
    assert content == ["line1", "line2"]


def test_save_to_file_overwrite(tmp_path):
    """Test that overwriting a file replaces its content.

    Args:
        tmp_path (pathlib.Path): Temporary directory provided by pytest.
    """
    file_path = tmp_path / "test.txt"

    save_to_file(file_path, "line1")
    save_to_file(file_path, "line2", overwrite=True)

    content = file_path.read_text().splitlines()
    assert content == ["line2"]


def test_save_to_file_creates_file(tmp_path):
    """Test that a new file is created if it does not exist.

    Args:
        tmp_path (pathlib.Path): Temporary directory provided by pytest.
    """
    file_path = tmp_path / "new.txt"
    save_to_file(file_path, "new_line")

    assert file_path.exists()
    assert file_path.read_text().strip() == "new_line"


def test_load_file_list_and_set():
    """Test loading a file both as a list and as a set.

    This test creates a temporary file with duplicate lines and verifies:
        * Loading as a list preserves duplicates and order.
        * Loading as a set removes duplicates.

    Raises:
        AssertionError: If list or set output is incorrect.
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
    """Test loading a non-existent file.

    Verifies:
        * Returns an empty list if `as_set=False`.
        * Returns an empty set if `as_set=True`.

    Raises:
        AssertionError: If return values are not empty list or set.
    """
    data_list = load_file("nonexistent_file.txt", as_set=False)
    assert data_list == []

    data_set = load_file("nonexistent_file.txt", as_set=True)
    assert data_set == set()


def test_save_to_file_and_load():
    """Test saving multiple lines and loading them back.

    This test:
        * Creates a temporary file.
        * Saves multiple lines using `save_to_file`.
        * Reloads the file using `load_file`.
        * Verifies that the lines match in correct order.

    Raises:
        AssertionError: If saved and loaded lines do not match.
    """
    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as tmp:
        tmp_path = tmp.name

    save_to_file(tmp_path, "combo1")
    save_to_file(tmp_path, "combo2")

    data = load_file(tmp_path)
    assert data == ["combo1", "combo2"]

    os.remove(tmp_path)
