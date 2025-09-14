import pytest
from unittest.mock import Mock
from requests.cookies import RequestsCookieJar
from utils.session_utils import fetch_login_form, extract_csrf
from settings import USERNAME_PARAM_STRING, PASSWORD_PARAM_STRING


@pytest.fixture
def mock_session():
    """
    Provide a dummy session object for testing login form fetching and POST requests.

    The session simulates:
        - GET requests to return a login form with a CSRF token.
        - POST requests to simulate login success/failure depending on credentials.

    Returns:
        DummySession: A mocked session object with `get` and `post` methods.
    """
    class DummySession:
        headers = {}
        cookies = {}

        def get(self, url, timeout=None):
            resp = Mock()
            resp.status_code = 200
            resp.cookies = {'dummy': 'cookie'}
            resp.text = '<form action="/login.cms"><input name="csrf_token" value="abc123"/></form>'
            return resp

        def post(self, url, data=None, timeout=None):
            resp = Mock()
            resp.status_code = 200

            if data[USERNAME_PARAM_STRING] == "admin" and data[PASSWORD_PARAM_STRING] == "123":
                resp.json.return_value = {"error": False}
            else:
                resp.json.return_value = {"error": True}
            resp.cookies = {}
            return resp

    return DummySession()


def test_create_session_success(monkeypatch):
    """
    Test that `create_session` returns a session with cookies when the server responds with 200.

    Args:
        monkeypatch: pytest fixture for patching attributes.
    """
    from utils.session_utils import create_session
    import requests

    class DummySession(requests.Session):
        def get(self, url, timeout=None):
            resp = requests.Response()
            resp.status_code = 200

            jar = RequestsCookieJar()
            jar.set("a", "b")
            resp._content = b""
            resp.cookies = jar
            return resp

    monkeypatch.setattr("requests.Session", DummySession)

    session = create_session()
    assert session is not None
    assert session.cookies.get("a") == "b"


def test_fetch_login_form_returns_action_and_values(mock_session):
    """
    Test that `fetch_login_form` correctly parses form action URL and input values.

    Args:
        mock_session: Dummy session fixture.
    """
    post_url, form_values = fetch_login_form(mock_session)
    assert post_url.endswith("/login.cms")
    assert form_values["csrf_token"] == "abc123"


def test_extract_csrf_returns_token():
    """
    Test that `extract_csrf` returns the correct CSRF token from multiple possible keys.
    """
    form_values = {"csrf_token": "abc123", "_csrf": "def456", "token": "ghi789"}
    token = extract_csrf(form_values)
    assert token == "abc123"

    token2 = extract_csrf({"_csrf": "def456"})
    assert token2 == "def456"

    token3 = extract_csrf({"token": "ghi789"})
    assert token3 == "ghi789"

    token4 = extract_csrf({})
    assert token4 is None
