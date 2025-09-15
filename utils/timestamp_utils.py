from datetime import datetime


def timestamp() -> str:
    """Return the current timestamp as a formatted string.

    The timestamp is formatted as ``[YYYY-MM-DD HH:MM:SS]`` using the
    current local time.

    Returns:
        str: The current timestamp in square brackets.
    """
    return datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
