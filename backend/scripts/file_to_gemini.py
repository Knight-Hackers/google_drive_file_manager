"""Fetch Drive file metadata/content and optionally send to Gemini for analysis.

Usage (PowerShell):
& ".venv/Scripts/Activate.ps1"
python backend/scripts/file_to_gemini.py --file-id <FILE_ID> [--metadata] [--download PATH] [--send-to-gemini]

Examples:
# Print metadata only
python backend/scripts/file_to_gemini.py --file-id 1AbC.. --metadata

# Download contents to local path
python backend/scripts/file_to_gemini.py --file-id 1AbC.. --download ./tmp.txt

# Send content to Gemini (requires GOOGLE_API_KEY env var)
python backend/scripts/file_to_gemini.py --file-id 1AbC.. --send-to-gemini

Notes:
- The script uses the project's FileManager to resolve credentials. Ensure GOOGLE_SERVICE_ACCOUNT_PATH or GOOGLE_SERVICE_ACCOUNT_JSON
  are configured and the service account has access to the files (shared or domain-wide delegation).
- For Google Docs/Sheets/Slides, the script exports to text/plain or CSV when downloading or sending to Gemini.
"""

import os
import io
import argparse
from pathlib import Path
from dotenv import load_dotenv
from typing import Optional

# ensure repo root in sys.path for package imports
import sys
REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

load_dotenv(dotenv_path=REPO_ROOT / '.env')

from backend.Agents.FileManager import FileManager
from googleapiclient.http import MediaIoBaseDownload

# Optional Gemini integration (if google genai is installed and GOOGLE_API_KEY is set)
try:
    from google import genai
except Exception:
    genai = None


def find_file_by_name(fm: FileManager, name: str) -> dict:
    """Search for a file by name and return its metadata."""
    # Build a query that matches filename exactly or contains the name
    q = f"name = '{name}' or name contains '{name}'"
    try:
        resp = fm.execute({"action": "list_files", "q": q, "page_size": 10})
        files = resp.get("files", [])
        if not files:
            print(f"No files found matching '{name}'")
            return None
        if len(files) > 1:
            print(f"\nFound {len(files)} matching files:")
            for i, f in enumerate(files, 1):
                print(f"{i:2d}. {f.get('name')} ({f.get('mimeType')})")
            while True:
                try:
                    choice = input("\nEnter number to select a file: ").strip()
                    idx = int(choice) - 1
                    if 0 <= idx < len(files):
                        return files[idx]
                except ValueError:
                    pass
                print("Invalid choice. Enter a number from the list.")
        return files[0]
    except Exception as e:
        print(f"Error searching for files: {e}")
        return None

def get_metadata(fm: FileManager, file_id: str) -> dict:
    """Get metadata for a file by its ID."""
    out = fm.execute({"action": "get_file", "file_id": file_id})
    return out.get("file")


def download_file_content(fm: FileManager, file_id: str, export_mime: Optional[str] = None) -> tuple[bytes, str]:
    """Download a file's content from Drive.

    Returns (bytes_content, filename)
    """
    service = fm._build_service()
    # get basic metadata to decide method
    meta = service.files().get(fileId=file_id, fields='id, name, mimeType').execute()
    mime = meta.get('mimeType')
    name = meta.get('name')

    fh = io.BytesIO()

    # Google Docs family: export
    if mime and mime.startswith('application/vnd.google-apps.'):
        # choose export mime based on type
        if mime == 'application/vnd.google-apps.document':
            out_mime = export_mime or 'text/plain'
        elif mime == 'application/vnd.google-apps.spreadsheet':
            out_mime = export_mime or 'text/csv'
        elif mime == 'application/vnd.google-apps.presentation':
            out_mime = export_mime or 'application/pdf'
        else:
            # generic fallback
            out_mime = export_mime or 'text/plain'
        request = service.files().export_media(fileId=file_id, mimeType=out_mime)
        downloader = MediaIoBaseDownload(fh, request)
    else:
        # regular file: download binary
        request = service.files().get_media(fileId=file_id)
        downloader = MediaIoBaseDownload(fh, request)

    done = False
    while not done:
        status, done = downloader.next_chunk()

    return fh.getvalue(), name


def send_text_to_gemini(text: str, model: str = 'gemini-2.5-flash') -> Optional[str]:
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        raise RuntimeError('GOOGLE_API_KEY (Gemini API key) not set in environment')
    if genai is None:
        raise RuntimeError('google.genai library not available in the environment')

    client = genai.Client(api_key=api_key)
    # The project-level helper in this repo uses models.generate_content; emulate that
    resp = client.models.generate_content(model=model, contents=text)
    # Attempt to return textual content (compat with earlier helper)
    try:
        return resp.text
    except Exception:
        # Fallback: the object may contain different fields
        return str(resp)


def find_files_by_name(fm: FileManager, name_query: str, max_results: int = 10) -> list:
    """Search for files by name in Drive. Returns list of {id, name, mimeType} dicts."""
    # Build a query that matches filename containing the search term (case-insensitive)
    q = f"name contains '{name_query}' and trashed = false"
    try:
        resp = fm.execute({"action": "list_files", "q": q, "page_size": max_results})
        return resp.get("files", [])
    except Exception as e:
        print(f"Failed to search files: {e}")
        return []


def interactive_file_picker(fm: FileManager) -> Optional[str]:
    """Let user search for files by name and pick one. Returns file_id or None."""
    while True:
        query = input("\nEnter part of filename to search (or 'q' to quit): ").strip()
        if query.lower() in ('q', 'quit', 'exit'):
            return None
        if not query:
            continue

        matches = find_files_by_name(fm, query)
        if not matches:
            print(f"No files found matching '{query}'")
            continue

        print(f"\nFound {len(matches)} matching files:")
        for i, f in enumerate(matches, 1):
            print(f"{i:2d}. {f.get('name')} ({f.get('mimeType')}) - id: {f.get('id')}")

        while True:
            choice = input("\nEnter number to select a file (or 'n' for new search): ").strip()
            if choice.lower() in ('n', 'new'):
                break
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(matches):
                    return matches[idx]['id']
            except ValueError:
                pass
            print("Invalid choice. Enter a number from the list or 'n' for new search.")


def main():
    p = argparse.ArgumentParser(description='Fetch Drive metadata/content and optionally send to Gemini')
    # Add example using a real file from your Drive
    p.add_argument('--file-id', help='Drive file id (if omitted, will prompt to search by name)')
    p.add_argument('--name', help='Search for files with this name (substring match)')
    p.add_argument('--metadata', action='store_true', help='Print metadata only')
    p.add_argument('--download', type=str, help='Write content to local path')
    p.add_argument('--send-to-gemini', action='store_true', help='Send file text content to Gemini (requires GOOGLE_API_KEY)')
    p.add_argument('--max-chars', type=int, default=30000, help='Max characters to send to Gemini (truncates)')
    p.add_argument('--list', action='store_true', help='List first 10 files in your Drive')

    if len(sys.argv) == 1:
        # No args - show examples with real files from the user's Drive
        fm = FileManager()
        print("\nExamples using files from your Drive:")
        resp = fm.execute({"action": "list_files", "page_size": 3})
        files = resp.get("files", [])
        if files:
            print("\nExample commands using your files:")
            for f in files[:3]:
                print(f"\n# Get metadata for '{f.get('name')}':")
                print(f"python {sys.argv[0]} --file-id {f.get('id')} --metadata")
            print("\n# Or search by name:")
            print(f"python {sys.argv[0]} --name \"document\" --send-to-gemini")
            print("\n# Or run in interactive mode (search and pick):")
            print(f"python {sys.argv[0]} --send-to-gemini")
        p.print_help()
        return

    args = p.parse_args()

    fm = FileManager()

    # Get file_id: either from args, or by searching, or via interactive picker
    file_id = args.file_id
    if not file_id and args.name:
        matches = find_files_by_name(fm, args.name)
        if matches:
            file_id = matches[0]['id']
            print(f"\nUsing first match: {matches[0]['name']} (id: {file_id})")
        else:
            print(f"No files found matching '{args.name}'")
            return
    if not file_id:
        file_id = interactive_file_picker(fm)
    if not file_id:
        return  # user quit or no file selected

    # If just listing files, do that and exit
    if args.list:
        resp = fm.execute({"action": "list_files", "page_size": 10})
        files = resp.get("files", [])
        print(f"\nFirst {len(files)} files in your Drive:")
        for i, f in enumerate(files, 1):
            print(f"{i:2d}. {f.get('name')} ({f.get('mimeType')})")
        return

    # Fetch metadata for the resolved file_id
    try:
        metadata = get_metadata(fm, file_id)
    except Exception as e:
        print('Failed to fetch metadata:', e)
        return

    print('\nMetadata:')
    for k, v in (metadata or {}).items():
        print(f'  {k}: {v}')

    if args.metadata and not args.download and not args.send_to_gemini:
        return

    # Download content for the resolved file_id
    try:
        content_bytes, name = download_file_content(fm, file_id)
    except Exception as e:
        print('Failed to download file content:', e)
        return

    # Attempt to decode as text for sending to Gemini; if binary, save to file if requested
    try:
        content_text = content_bytes.decode('utf-8')
    except Exception:
        content_text = None

    if args.download:
        out_path = Path(args.download)
        if content_text is not None:
            out_path.write_text(content_text, encoding='utf-8')
            print(f'Wrote text content to {out_path}')
        else:
            out_path.write_bytes(content_bytes)
            print(f'Wrote binary content to {out_path}')

    if args.send_to_gemini:
        try:
            print(f"Sending file '{metadata.get('name')}' (id={file_id}) to Gemini (model=gemini-2.5-flash)...")
            out = fm.send_file_to_gemini(file_id, model='gemini-2.5-flash', max_chars=args.max_chars)
            print('\nGemini response:\n')
            print(out)
        except Exception as e:
            print('Failed to send to Gemini:', e)


if __name__ == '__main__':
    main()
