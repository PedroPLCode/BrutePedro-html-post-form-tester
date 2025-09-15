from typing import Set
from utils.timestamp_utils import timestamp
from settings import SUCCESS_FILE_PATH, bold_text, green_bold, reset_text


def create_results_summary(known_success: Set[str], success: bool) -> str:
    """Build a multi-line summary of brute-force results.

    This function constructs a human-readable, timestamped summary describing
    results of a brute-force run. It **returns** the formatted summary string;
    the caller may print it, log it, or write it to a file.

    Args:
        known_success (Set[str]): Set of successful "username:password" combos.
        success (bool): Indicates if any attempt was considered successful
            (useful if detection is separate from saved results).

    Returns:
        str: Multiline summary containing timestamps and colored/styled text.
    """
    if known_success or success:
        return (
            f"{timestamp()} {green_bold}[*] Successful combinations found: {len(known_success)}{reset_text}\n"
            f"{timestamp()} {green_bold}[*] All successful combinations saved in {SUCCESS_FILE_PATH}.{reset_text}\n"
            f"{timestamp()} {bold_text}[?] Possible false positives, please verify manually.{reset_text}"
        ) 
    return f"{timestamp()} {bold_text}[*] No successful combinations found.{reset_text}"
