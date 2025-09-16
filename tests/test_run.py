from unittest.mock import patch, Mock
from run import run_brute_force
from settings import (
    USERNAMES_FILE_PATH,
    PASSWORDS_FILE_PATH,
    SUCCESS_FILE_PATH,
    PROGRESS_FILE_PATH,
)


def test_run_brute_force_success(tmp_path):
    """
    Test the run_brute_force function for successful login attempts.

    This test mocks file I/O and network calls to simulate a brute-force
    scenario. It verifies that all username:password combinations are
    attempted and recorded in the known_success set, and that progress
    is saved during execution.

    Args:
        tmp_path: pytest temporary path fixture for creating temporary files.

    Assertions:
        - All username:password combinations are added to known_success.
        - The save_to_file function is called to save progress.
    """
    known_success = set()
    usernames = ["user1", "user2", "user3", "user4", "user5"]
    passwords = ["pass1", "pass2", "pass3", "pass4", "pass5"]

    def load_file_side_effect(filepath, as_set=False):
        if filepath == SUCCESS_FILE_PATH:
            return known_success
        elif filepath == PROGRESS_FILE_PATH:
            return []
        elif filepath == USERNAMES_FILE_PATH:
            return usernames
        elif filepath == PASSWORDS_FILE_PATH:
            return passwords
        return []

    with patch("run.create_session") as mock_create_session, patch(
        "run.load_file", side_effect=load_file_side_effect
    ), patch("run.save_to_file") as mock_save, patch("run.try_login") as mock_try_login:

        mock_create_session.return_value = Mock()

        def try_login_side_effect(session, known, username, password, attempt_counter):
            """Mock try_login to always succeed and add to known_success."""
            known.add(f"{username}:{password}")
            return True, attempt_counter + 1

        mock_try_login.side_effect = try_login_side_effect

        run_brute_force()

        for u in usernames:
            for p in passwords:
                assert f"{u}:{p}" in known_success
        assert mock_save.called
