from datetime import datetime
import re
from utils.timestamp_utils import timestamp


def test_timestamp_is_parsable() -> None:
    """Test that timestamp() produces a valid datetime string.

    This test ensures that the string returned by timestamp() is:
      * of type str
      * properly formatted so it can be parsed by datetime.strptime()
        using the format "[%Y-%m-%d %H:%M:%S]".

    Raises:
        AssertionError: If the return value is not a str or cannot be parsed.
    """
    ts = timestamp()
    assert isinstance(ts, str)
    datetime.strptime(ts, "[%Y-%m-%d %H:%M:%S]")


def test_timestamp_matches_regex() -> None:
    """Test that timestamp() matches the expected regex format.

    This test verifies that the string returned by timestamp() matches
    the pattern ``[YYYY-MM-DD HH:MM:SS]``.

    Raises:
        AssertionError: If the timestamp string does not match the regex.
    """
    ts = timestamp()
    pattern = r"^\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\]$"
    assert re.match(pattern, ts)
