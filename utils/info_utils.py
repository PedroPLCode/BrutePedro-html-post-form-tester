from typing import Set
from datetime import datetime
from settings import SUCCESS_FILE_PATH, bold_text, green_bold, reset_text


def timestamp() -> str:
    """Return the current timestamp as a formatted string.

    The timestamp is formatted as ``[YYYY-MM-DD HH:MM:SS]`` using the
    current local time.

    Returns:
        str: The current timestamp in square brackets.
    """
    return datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")


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
        f"{timestamp()} {bold_text}[*] BrutePedro out for the day!{reset_text}"
    )

    return "".join(results_summary)
