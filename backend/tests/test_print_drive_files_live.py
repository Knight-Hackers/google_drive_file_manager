import os
import pytest

# This test intentionally performs a live call to Google Drive. It is disabled by default
# to avoid accidental network calls or credential use. To enable, set the environment variable:
#   RUN_LIVE_GDRIVE_TESTS=1
# and ensure GOOGLE_SERVICE_ACCOUNT_PATH or GOOGLE_SERVICE_ACCOUNT_JSON is configured.

RUN_LIVE = os.getenv("RUN_LIVE_GDRIVE_TESTS", "").lower() in ("1", "true", "yes")

pytestmark = pytest.mark.skipif(not RUN_LIVE, reason="Live Google Drive tests disabled. Set RUN_LIVE_GDRIVE_TESTS=1 to enable.")

from backend.Agents.FileManager import FileManager


def test_print_drive_files_live():
    """Live test: list files from Google Drive and print a few entries.

    This test will attempt to use the FileManager which reads credentials from:
    - GOOGLE_SERVICE_ACCOUNT_PATH (preferred) OR
    - GOOGLE_SERVICE_ACCOUNT_JSON (raw JSON)

    The test only asserts that a list is returned; its main purpose is to print results
    for manual inspection.
    """
    fm = FileManager()

    # Request the first page of files. Adjust page_size if you want more/less output.
    out = fm.execute({"action": "list_files", "page_size": 50})
    files = out.get("files", [])

    print(f"\nLive Drive test: found {len(files)} files (showing up to 50):\n")
    for i, f in enumerate(files[:50], start=1):
        print(f"{i:2d}. id={f.get('id')} name={f.get('name')} mimeType={f.get('mimeType')}")

    assert isinstance(files, list)
