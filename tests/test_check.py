import pytest
from unittest.mock import patch, MagicMock
from check import check_server_before_brute_force
from settings import DUMMY_USERNAME, DUMMY_PASSWORD


class MockSession:
    """Mock session object for simulating HTTP requests."""

    def post(self, url, data=None, timeout=None):
        """Simulate a successful POST request."""
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            "success": True,
            "message": "Test login successful",
        }
        return mock_resp


@pytest.fixture
def mock_session_create():
    """Fixture to mock the session creation function.

    Yields:
        MagicMock: Mocked session creation function returning a MockSession.
    """
    with patch(
        "utils.session_utils.create_session", return_value=MockSession()
    ) as mock_create:
        yield mock_create


@pytest.fixture
def mock_fetch_login_form():
    """Fixture to mock the login form fetching function.

    Yields:
        MagicMock: Mocked function returning a dummy login URL and form values.
    """
    with patch(
        "utils.session_utils.fetch_login_form",
        return_value=(
            "http://example.com/login",
            {"redirect": "/dashboard", "csrf_token": "dummy_csrf"},
        ),
    ) as mock_fetch:
        yield mock_fetch


@pytest.fixture
def mock_extract_csrf():
    """Fixture to mock CSRF token extraction.

    Yields:
        MagicMock: Mocked function returning a dummy CSRF token.
    """
    with patch(
        "utils.session_utils.extract_csrf", return_value="dummy_csrf"
    ) as mock_csrf:
        yield mock_csrf


def test_check_server_success(
    mock_session_create, mock_fetch_login_form, mock_extract_csrf, capsys
):
    """Test successful execution of server check.

    Verifies that the server check function prints expected debug output
    including payload and dummy credentials.

    Args:
        mock_session_create (fixture): Mocked session creation.
        mock_fetch_login_form (fixture): Mocked login form fetch.
        mock_extract_csrf (fixture): Mocked CSRF token extraction.
        capsys (pytest fixture): Capture system output.
    """
    check_server_before_brute_force()
    captured = capsys.readouterr()
    assert "Server checks completed" in captured.out
    assert DUMMY_USERNAME in captured.out
    assert DUMMY_PASSWORD in captured.out
    assert "payload" in captured.out


def test_check_server_session_fail(capsys):
    """Test behavior when session creation fails.

    Verifies that the appropriate failure message is printed when
    the session cannot be created.

    Args:
        capsys (pytest fixture): Capture system output.
    """
    with patch("check.create_session", return_value=None):
        check_server_before_brute_force()
    captured = capsys.readouterr()
    assert "Failed to create session" in captured.out


def test_check_server_invalid_json(capsys):
    """Test handling of non-JSON server response.

    Verifies that the server check prints a warning message when
    the response cannot be parsed as JSON.

    Args:
        capsys (pytest fixture): Capture system output.
    """

    class MockBadJSONSession:
        """Mock session that raises ValueError when calling .json()."""

        def post(self, url, data=None, timeout=None):
            mock_resp = MagicMock()
            mock_resp.status_code = 200
            mock_resp.json.side_effect = ValueError("No JSON")
            return mock_resp

    with patch("check.create_session", return_value=MockBadJSONSession()), patch(
        "check.fetch_login_form",
        return_value=("http://example.com/login", {"redirect": "/dashboard"}),
    ), patch("check.extract_csrf", return_value=None):
        check_server_before_brute_force()
    captured = capsys.readouterr()
    assert "Response is not valid JSON" in captured.out
