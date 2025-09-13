import pytest
from unittest.mock import patch, Mock
from utils.brute_utils import create_session, get_csrf_token, try_login

@pytest.fixture
def mock_session():
    """Creates a mocked requests.Session object."""
    mock_sess = Mock()
    return mock_sess

def test_create_session_success():
    with patch("utils.brute_utils.requests.Session.get") as mock_get:
        mock_resp = Mock()
        mock_resp.status_code = 200
        mock_get.return_value = mock_resp
        session = create_session()
        assert session is not None

def test_create_session_failure():
    with patch("utils.brute_utils.requests.Session.get") as mock_get:
        mock_resp = Mock()
        mock_resp.status_code = 500
        mock_get.return_value = mock_resp
        session = create_session()
        assert session is None

def test_get_csrf_token_found(mock_session):
    html = '<input type="hidden" name="csrf_token" value="12345">'
    mock_resp = Mock()
    mock_resp.text = html
    mock_session.get.return_value = mock_resp
    token = get_csrf_token(mock_session)
    assert token == "12345"

def test_get_csrf_token_not_found(mock_session):
    html = '<html></html>'
    mock_resp = Mock()
    mock_resp.text = html
    mock_session.get.return_value = mock_resp
    token = get_csrf_token(mock_session)
    assert token is None

def test_try_login_success(mock_session, tmp_path):
    known_success = set()
    html_token = '<input type="hidden" name="csrf_token" value="12345">'
    mock_session.get.return_value.text = html_token

    mock_resp_post = Mock()
    mock_resp_post.json.return_value = {"error": False}
    with patch.object(mock_session, "post", return_value=mock_resp_post):
        from utils.brute_utils import SUCCESS_FILE
        success_file = tmp_path / "success.txt"
        with patch("utils.brute_utils.SAVE_FILE", new=success_file):
            result = try_login(mock_session, known_success, "user", "pass")
            assert result is True
            assert "user:pass" in known_success
