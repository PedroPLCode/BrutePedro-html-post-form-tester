import pytest
from unittest.mock import patch, Mock
from run import run_brute_force
from settings import USERNAMES_FILE, PASSWORDS_FILE, SUCCESS_FILE, PROGRESS_FILE

def test_run_brute_force_success(tmp_path):
    known_success = set()
    usernames = ["user1", "user2"]
    passwords = ["pass1", "pass2"]

    def load_file_side_effect(filepath, as_set=False):
        if filepath == SUCCESS_FILE:
            return known_success
        elif filepath == PROGRESS_FILE:
            return []
        elif filepath == USERNAMES_FILE:
            return usernames
        elif filepath == PASSWORDS_FILE:
            return passwords
        return []

    # Mock create_session, load_file, save_to_file, try_login
    with patch("run.create_session") as mock_create_session, \
         patch("run.load_file", side_effect=load_file_side_effect), \
         patch("run.save_to_file") as mock_save, \
         patch("run.try_login") as mock_try_login:

        mock_create_session.return_value = Mock()

        def try_login_side_effect(session, known, username, password):
            known.add(f"{username}:{password}")
            return True

        mock_try_login.side_effect = try_login_side_effect

        # Run the brute-force
        run_brute_force()

        # Assertions
        for u in usernames:
            for p in passwords:
                assert f"{u}:{p}" in known_success
        assert mock_save.called
