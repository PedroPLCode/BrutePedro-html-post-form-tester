import json
from typing import Set
from datetime import datetime
from settings import  (
    bold_text,
    green_bold,
    reset_text,
    HEADERS,
    LOGIN_PAGE_URL,
    LOGIN_POST_URL,
    REDIRECT_URL,
    DELAY_BETWEEN_REQUESTS,
    MAX_ATTEMPTS_PER_SESSION,
    SUCCESS_FILE_PATH,
)


def timestamp() -> str:
    """
    Return the current timestamp as a formatted string.

    The timestamp is formatted as ``[YYYY-MM-DD HH:MM:SS]`` using the
    current local time.

    Returns:
        str: The current timestamp in square brackets.
    """
    return datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")


def create_welcome_message() -> str:
    """
    Build a multi-line welcome message for the brute-force attack.
    
    This function generates a welcome message that includes details about
    the target URL, login POST URL, redirect URL, headers, delay between
    requests, and maximum attempts per session.
    
    Returns:
        str: A formatted multi-line welcome message.
    """
    return (f"{bold_text}BrutePedro - html-post-form brute-force tester v1.0{reset_text}\n"
          f"{timestamp()} [*] Hello world! Let's get started with the brute-force attack!\n"
          f"{timestamp()} [*] Target URL: {bold_text}{LOGIN_PAGE_URL}{reset_text}\n"
          f"{timestamp()} [*] Login POST URL: {bold_text}{LOGIN_POST_URL}{reset_text}\n"
          f"{timestamp()} [*] Redirect URL: {bold_text}{REDIRECT_URL}{reset_text}\n"
          f"{timestamp()} [*] Headers: {bold_text}{json.dumps(HEADERS, indent=2, ensure_ascii=False)}{reset_text}\n"
          f"{timestamp()} [*] Delay between requests: {bold_text}{DELAY_BETWEEN_REQUESTS} seconds{reset_text}\n"
          f"{timestamp()} [*] Max attempts per session: {bold_text}{MAX_ATTEMPTS_PER_SESSION}{reset_text}\n"
          f"{timestamp()} [*] Dynamic session management enabled.{reset_text}\n"
          f"{timestamp()} [*] Starting attack... Press Ctrl+C to stop and save progress.")


def create_results_summary(known_success: Set[str], possible_success: bool) -> str:
    """Build a multi-line summary of brute-force results.

    This function generates a summary of the brute-force attack results,
    including the number of successful combinations found and whether there
    were any ambiguous results that may require manual verification.

    Args:
        known_success (Set[str]): Set of successful "username:password" combos.
        possible_success (bool): Whether any attempts had ambiguous results.

    Returns:
        str: A formatted multi-line summary of the brute-force results.
    """
    results_summary: list[str] = []

    if known_success or possible_success:
        results_summary.append(
            f"{timestamp()} {green_bold}[*] Successful combinations found: {len(known_success)}{reset_text}\n"
            f"{timestamp()} {green_bold}[*] All successful combinations saved in {SUCCESS_FILE_PATH}.{reset_text}\n"
            f"{timestamp()} {bold_text}[?] Possible false positives, please verify manually.{reset_text}\n"
        )
    else:
        results_summary.append(
            f"{timestamp()} {bold_text}[*] No successful combinations found. What a shame...{reset_text}\n"
            f"{timestamp()} {bold_text}[*] Better luck next time!{reset_text}\n"
            f"{timestamp()} {bold_text}[*] Try with different credentials.{reset_text}\n"
        )
        
    results_summary.append(
        f"{timestamp()} [*] BrutePedro out for the day!"
    )

    return "".join(results_summary)
