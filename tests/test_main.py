import sys
from unittest.mock import patch, MagicMock
import pytest
import main


def test_main_attack(monkeypatch):
    """Test that main() calls attack.run_brute_force_attack() when mode='attack'.

    This ensures that the attack module is executed correctly
    when the 'attack' mode is passed to the main function.

    Args:
        monkeypatch (pytest.MonkeyPatch): Fixture to patch modules dynamically.
    """
    mock_attack = MagicMock()
    monkeypatch.setitem(sys.modules, "core.attack", mock_attack)

    main.main("attack")
    mock_attack.run_brute_force_attack.assert_called_once()


def test_main_check(monkeypatch):
    """Test that main() calls check.check_server_before_brute_force() when mode='check'.

    This ensures that the check module is executed correctly
    when the 'check' mode is passed to the main function.

    Args:
        monkeypatch (pytest.MonkeyPatch): Fixture to patch modules dynamically.
    """
    mock_check = MagicMock()
    monkeypatch.setitem(sys.modules, "core.check", mock_check)

    main.main("check")
    mock_check.check_server_before_brute_force.assert_called_once()


def test_main_invalid_mode(capsys):
    """Test that main() prints an error message on invalid mode.

    This verifies that the main function handles invalid mode arguments
    by printing an appropriate error message.

    Args:
        capsys (pytest.CaptureFixture): Fixture to capture stdout/stderr output.
    """
    main.main("invalid_mode")
    captured = capsys.readouterr()
    assert "Invalid mode" in captured.out


def test_main_cli_usage(capsys):
    """Test that CLI usage message is printed when no arguments are provided.

    This ensures that the script exits with a SystemExit and prints the
    usage instructions if run without the required command-line argument.

    Args:
        capsys (pytest.CaptureFixture): Fixture to capture stdout/stderr output.
    """
    test_argv = ["main.py"]
    with patch.object(sys, "argv", test_argv):
        with pytest.raises(SystemExit):
            import main

            main.cli()
    captured = capsys.readouterr()
    assert "Usage: python main.py" in captured.out
