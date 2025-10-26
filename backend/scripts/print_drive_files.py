"""Print files from Google Drive using the project's FileManager tool.

Usage (PowerShell / Windows):

# activate venv first (example)
& ".venv/Scripts/Activate.ps1"
# run script (reads .env automatically)
python backend/scripts/print_drive_files.py --page-size 50

Environment:
- Set `GOOGLE_SERVICE_ACCOUNT_PATH` to your service account JSON key file (recommended)
  OR
- Set `GOOGLE_SERVICE_ACCOUNT_JSON` to the raw JSON string of the key (no extra surrounding quotes).

Notes:
- The service account must have access to the Drive files you want to list (shared with the service account or domain-wide delegation configured).
- This script will try to load `.env` automatically (python-dotenv).
"""

import os
import json
import argparse
from dotenv import load_dotenv

# ensure package path resolution can import backend.Agents
import sys
from pathlib import Path

# add repo root to sys.path so imports work when running script from repo root
REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

load_dotenv(dotenv_path=REPO_ROOT / '.env')

from backend.Agents.FileManager import FileManager


def main():
    parser = argparse.ArgumentParser(description='Print Google Drive files via FileManager')
    parser.add_argument('--q', type=str, default="trashed = false", help='Drive API query string (q)')
    parser.add_argument('--page-size', type=int, default=100, help='Number of items to request per page')
    parser.add_argument('--max', type=int, default=100, help='Maximum number of files to print (script will stop after this many)')
    parser.add_argument('--out', type=str, default=None, help='Optional output JSON file to write (full list)')
    args = parser.parse_args()

    print(f"Using repo root: {REPO_ROOT}")
    print("Reading credentials from environment: ")
    print("  - GOOGLE_SERVICE_ACCOUNT_PATH=", os.getenv('GOOGLE_SERVICE_ACCOUNT_PATH'))
    # don't print raw JSON for security
    print("  - GOOGLE_SERVICE_ACCOUNT_JSON set? ", bool(os.getenv('GOOGLE_SERVICE_ACCOUNT_JSON')))

    fm = FileManager()

    try:
        resp = fm.execute({'action': 'list_files', 'q': args.q, 'page_size': args.page_size})
    except Exception as e:
        print('Failed to list files:', e)
        return

    files = resp.get('files', [])

    # Optionally write JSON output
    if args.out:
        with open(args.out, 'w', encoding='utf-8') as fh:
            json.dump(files, fh, indent=2, ensure_ascii=False)
        print(f'Wrote {len(files)} items to {args.out}')

    # Pretty-print up to --max items
    print(f"\nFound {len(files)} files (showing up to {args.max}):\n")
    for i, f in enumerate(files[: args.max], start=1):
        print(f"{i:3d}. id={f.get('id')!s:38} name={f.get('name')!s} mimeType={f.get('mimeType')!s} size={f.get('size')})")

## NOTE: f.get('name') is how we access the file type. 

if __name__ == '__main__':
    main()
