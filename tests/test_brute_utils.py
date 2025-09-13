import pytest
from unittest.mock import patch, Mock
from utils.brute_utils import create_session, get_csrf_token, try_login


@pytest.fixture
def mock_session():
    """
    Creates a mocked requests.Session object.

    Returns:
        Mock: A mocked session object.
    """
    mock_sess = Mock()
    return mock_sess


def test_create_session_success():
    """
    Test that create_session returns a valid session when the server
    responds with status code 200.
    """
    with patch("utils.brute_utils.requests.Session.get") as mock_get:
        mock_resp = Mock()
        mock_resp.status_code = 200
        mock_get.return_value = mock_resp
        session = create_session()
        assert session is not None


def test_create_session_failure():
    """
    Test that create_session returns None when the server responds
    with a non-200 status code.
    """
    with patch("utils.brute_utils.requests.Session.get") as mock_get:
        mock_resp = Mock()
        mock_resp.status_code = 500
        mock_get.return_value = mock_resp
        session = create_session()
        assert session is None


def test_get_csrf_token_found(mock_session):
    """
    Test that get_csrf_token correctly retrieves the CSRF token
    from the HTML of the login page.

    Args:
        mock_session (Mock): Mocked HTTP session.
    """
    html = '<input type="hidden" name="csrf_token" value="12345">'
    mock_resp = Mock()
    mock_resp.text = html
    mock_session.get.return_value = mock_resp
    token = get_csrf_token(mock_session)
    assert token == "12345"


def test_get_csrf_token_not_found(mock_session):
    """
    Test that get_csrf_token returns None when no CSRF token
    input is present in the HTML.

    Args:
        mock_session (Mock): Mocked HTTP session.
    """
    html = "<html></html>"
    mock_resp = Mock()
    mock_resp.text = html
    mock_session.get.return_value = mock_resp
    token = get_csrf_token(mock_session)
    assert token is None


def test_try_login_success(mock_session, tmp_path):
    """
    Test try_login function for a successful login scenario.

    This test mocks the session, CSRF token retrieval, and POST
    request, and verifies that the combination is added to the
    known_success set and saved to the file.

    Args:
        mock_session (Mock): Mocked HTTP session.
        tmp_path (Path): Temporary path provided by pytest.
    """
    known_success = set()
    html_token = '<input type="hidden" name="csrf_token" value="12345">'
    mock_session.get.return_value.text = html_token

    mock_resp_post = Mock()
    mock_resp_post.json.return_value = {"error": False}
    mock_session.post.return_value = mock_resp_post

    success_file_path = tmp_path / "success.txt"

    with patch("utils.brute_utils.save_to_file") as mock_save:

        def write_mock(filepath, combo):
            with open(success_file_path, "a") as f:
                f.write(combo + "\n")

        mock_save.side_effect = write_mock

        result = try_login(mock_session, known_success, "user", "pass")

    assert result is True
    assert "user:pass" in known_success

    content = success_file_path.read_text().strip()
    assert content == "user:pass"
