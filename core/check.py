import json
from typing import Any, Dict
from utils.info_utils import timestamp
from utils.session_utils import (
    create_session,
    fetch_login_form,
    extract_csrf
)
from settings import (
    REDIRECT_URL,
    USERNAME_PARAM_STRING,
    PASSWORD_PARAM_STRING,
    CSRF_PARAM_STRING,
    REDIRECT_PARAM_STRING,
    DUMMY_USERNAME,
    DUMMY_PASSWORD,
    bold_text,
    red_bold,
    reset_text
)


def check_server_before_brute_force() -> None:
    """Perform preliminary server checks before starting brute force attempts.

    This function:
        - Creates a new session.
        - Fetches the login form and extracts relevant parameters.
        - Builds a payload with dummy credentials and optional CSRF token.
        - Sends a test login request to the server.
        - Prints debug information about the request and response.

    Raises:
        SystemExit: If an unexpected error occurs during execution.
    """
    
    print (f"{bold_text}BrutePedro - html-post-form brute-force tester v1.0{reset_text}\n"
          f"{timestamp()} [*] Hello world! Let's check server and response before brute-force attack.")
        
    try:
        session = create_session()
        if not session:
            print(f"{timestamp()} {red_bold}[CHECK] Failed to create session.{reset_text}")
            return

        post_url, form_values = fetch_login_form(session)
        print(f"{timestamp()} [CHECK] post_url: {post_url}\n"
              f"{timestamp()} [CHECK] form_values: {form_values}")

        payload: Dict[str, Any] = {
            USERNAME_PARAM_STRING: DUMMY_USERNAME,
            PASSWORD_PARAM_STRING: DUMMY_PASSWORD,
            REDIRECT_PARAM_STRING: form_values.get(REDIRECT_PARAM_STRING, REDIRECT_URL),
        }
        csrf_val: str | None = extract_csrf(form_values)
        if csrf_val:
            payload[CSRF_PARAM_STRING] = csrf_val
        print(f"{timestamp()} [CHECK] payload: {payload}")

        resp = session.post(post_url, data=payload, timeout=15)
        print(f"{timestamp()} [CHECK] resp.status_code: {resp.status_code}")

        try:
            response_json: Dict[str, Any] = resp.json()
            pretty_json = json.dumps(response_json, indent=4, ensure_ascii=False)
            print(f"{timestamp()} [CHECK] response_json:\n{pretty_json}")
        except ValueError:
            print(f"{timestamp()} {red_bold}[CHECK] Response is not valid JSON.{reset_text}")

    except Exception as e:
        print(f"\n{timestamp()} {red_bold}[CHECK] An unexpected error occurred: {e}{reset_text}")
        raise SystemExit(1)

    print(f"{timestamp()} {bold_text}[CHECK] Server checks completed.{reset_text}")


if __name__ == "__main__":
    check_server_before_brute_force()
