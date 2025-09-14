import pytest
from unittest.mock import Mock
from utils.brute_utils import try_login
from settings import USERNAME_PARAM_STRING, PASSWORD_PARAM_STRING


@pytest.fixture
def mock_session():
    """
    Create a dummy HTTP session for testing `try_login`.

    The session simulates GET requests to fetch a login form with a CSRF token,
    and POST requests to simulate login attempts with configurable success/failure.
    
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


def test_try_login_success(mock_session):
    """
    Test `try_login` function for a successful login attempt.

    Verifies that:
        - The function returns True.
        - The successful credential combo is added to the known_success set.
        - The attempt counter is incremented correctly.
    """
    known = set()
    success, counter = try_login(mock_session, known, "admin", "123", 0)
    assert success is True
    assert "admin:123" in known
    assert counter == 1


def test_try_login_failure(mock_session):
    """
    Test `try_login` function for a failed login attempt.

    Verifies that:
        - The function returns False.
        - The failed credential combo is NOT added to the known_success set.
        - The attempt counter is incremented correctly.
    """
    known = set()
    success, counter = try_login(mock_session, known, "user", "wrong", 0)
    assert success is False
    assert "user:wrong" not in known
    assert counter == 1
