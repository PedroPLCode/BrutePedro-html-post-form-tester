import re
from typing import Set
import utils.info_utils as summary
from settings import SUCCESS_FILE_PATH, bold_text, green_bold, reset_text


def test_success_summary_with_results(monkeypatch) -> None:
    """Test that the summary contains success information when results exist.

    This test verifies:
    - the count of successful combinations is present and correct,
    - the saved-file message is present,
    - the "possible false positives" warning is present,
    - color/style tokens from settings are included.
    """
    monkeypatch.setattr(summary, "timestamp", lambda: "[2025-09-15 12:00:00]")
    known_success: Set[str] = {"user1:pass1", "user2:pass2"}
    result = summary.create_results_summary(known_success, success=True)

    assert isinstance(result, str)
    assert "[2025-09-15 12:00:00]" in result
    assert f"[*] Successful combinations found: {len(known_success)}" in result
    assert f"All successful combinations saved in {SUCCESS_FILE_PATH}" in result
    assert "Possible false positives" in result
    assert green_bold in result
    assert bold_text in result
    assert reset_text in result

    timestamps = re.findall(r"\[2025-09-15 12:00:00\]", result)
    assert len(timestamps) == 3


def test_success_summary_no_results(monkeypatch) -> None:
    """Test that the summary reports no results when none found.

    This test verifies:
    - the "No successful combinations found" message is returned,
    - formatting tokens (bold, reset) are included,
    - there is exactly one timestamped line.
    """
    monkeypatch.setattr(summary, "timestamp", lambda: "[2025-09-15 12:00:00]")
    known_success: Set[str] = set()
    result = summary.create_results_summary(known_success, success=False)

    assert isinstance(result, str)
    assert "[2025-09-15 12:00:00]" in result
    assert "No successful combinations found" in result
    assert bold_text in result
    assert reset_text in result

    timestamps = re.findall(r"\[2025-09-15 12:00:00\]", result)
    assert len(timestamps) == 1
