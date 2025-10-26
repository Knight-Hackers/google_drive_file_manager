from dotenv import load_dotenv
import os
from BaseTool import BaseTool
from typing import Dict, Any, List, Optional
import json
from googleapiclient.discovery import build
import io
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
import json
from pathlib import Path

load_dotenv()

class FileManager(BaseTool):

    """
    Agent that gathers cloud/drive data
    Helper tool for gemini so that it can organize files based on properties
    (e.g. name, size, date, contents).
    """

    def __init__(self):
        super().__init__(name="File Manager", description="Drive file manager tool", supported_file_types=None)
        # Default Drive API scopes we need
        self.scopes = [
            'https://www.googleapis.com/auth/drive.readonly',
            'https://www.googleapis.com/auth/drive.metadata.readonly'
        ]

        # Allow override via env vars
        self.service_account_path = os.getenv('GOOGLE_SERVICE_ACCOUNT_PATH')
        self.service_account_json = os.getenv('GOOGLE_SERVICE_ACCOUNT_JSON')
        # lazy-initialized service
        self._service = None

    def _build_service(self):
        """
        Create a Google Drive service using the user's OAuth2 tokens (not a service account).

        Expects a tokens.json file that contains 'access_token' and 'refresh_token'.
        Automatically refreshes the access token if expired.
        """
        if self._service:
            return self._service

        BASE_DIR = Path(__file__).resolve().parent
        TOKEN_PATH = BASE_DIR / "tokens.json"
        if not os.path.exists(TOKEN_PATH):
            raise RuntimeError("No user tokens found. Please authenticate via /user/login first.")

        with open(TOKEN_PATH, "r") as f:
            tokens = json.load(f)

        # Build credentials object using user's tokens
        creds = Credentials(
            token=tokens.get("access_token"),
            refresh_token=tokens.get("refresh_token"),
            token_uri="https://oauth2.googleapis.com/token",
            client_id="1036975395025-cr4f5c03p4o3v38a7m4tnsllja3njl0v.apps.googleusercontent.com",
            client_secret="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",
            scopes=self.scopes
        )

        # Refresh automatically if expired
        if not creds.valid:
            if creds.expired and creds.refresh_token:
                creds.refresh(Request())
                # Save the new access token back to tokens.json
                with open(TOKEN_PATH, "w") as f:
                    json.dump({
                        "access_token": creds.token,
                        "refresh_token": creds.refresh_token,
                        "expiry": creds.expiry.isoformat() if creds.expiry else None
                    }, f, indent=2)

        # Build the Drive API client
        self._service = build("drive", "v3", credentials=creds)
        return self._service

    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Generic executor. Expects payload with an 'action' key.

        Supported actions:
        - list_files: returns files matching optional 'q' and 'page_size'
        - count_files: returns {'count': int} for optional 'q'
        - get_file: requires 'file_id', returns metadata
        - list_folder: requires 'folder_id'
        """
        action = payload.get('action')
        if not action:
            raise ValueError("payload must include 'action'")

        if action == 'list_files':
            q = payload.get('q', "trashed = false")
            page_size = int(payload.get('page_size', 100))
            return {'files': self.list_files(q=q, page_size=page_size)}

        if action == 'count_files':
            q = payload.get('q', "trashed = false")
            return {'count': self.get_file_count(q=q)}

        if action == 'get_file':
            file_id = payload.get('file_id')
            if not file_id:
                raise ValueError('file_id is required for get_file')
            return {'file': self.get_file_metadata(file_id)}

        if action == 'list_folder':
            folder_id = payload.get('folder_id')
            if not folder_id:
                raise ValueError('folder_id is required for list_folder')
            return {'files': self.list_files(q=f"'{folder_id}' in parents and trashed = false")}

        if action == 'retreive_file':
            file_id = payload.get('file_id')
            if not file_id: 
                raise ValueError('file_id is required for retreive_file')
            return {'file': self.retrieve_file(file_id=file_id)}

        raise ValueError(f'Unknown action: {action}')

    def get_file_count(self, q: Optional[str] = None) -> int:
        service = self._build_service()
        q = q or "trashed = false"
        page_token = None
        count = 0
        while True:
            resp = service.files().list(q=q, spaces='drive', fields='nextPageToken, files(id)', pageSize=1000, pageToken=page_token).execute()
            files = resp.get('files', [])
            count += len(files)
            page_token = resp.get('nextPageToken')
            if not page_token:
                break
        return count

    def list_files(self, q: Optional[str] = None, page_size: int = 100) -> List[Dict[str, Any]]:
        service = self._build_service()
        q = q or "trashed = false"
        results: List[Dict[str, Any]] = []
        page_token = None
        fields = 'nextPageToken, files(id, name, mimeType, parents, md5Checksum, size, modifiedTime)'
        while True:
            resp = service.files().list(q=q, spaces='drive', fields=fields, pageSize=page_size, pageToken=page_token).execute()
            results.extend(resp.get('files', []))
            page_token = resp.get('nextPageToken')
            if not page_token:
                break
        return results

    def get_file_metadata(self, file_id: str) -> Dict[str, Any]:
        service = self._build_service()
        return service.files().get(fileId=file_id, fields='id, name, mimeType, parents, md5Checksum, size, createdTime, modifiedTime').execute()

    def retrieve_file(self, file_id: str, export_mime: Optional[str] = None) -> tuple[Any, str, str]:
        """Get a media request for a Drive file without downloading it.
        
        Returns (request, filename, mimetype) where request can be used with MediaIoBaseDownload
        or passed to other APIs that accept Drive file content. For Google Docs/Sheets/Slides,
        will export to sensible formats by default (text/plain for Docs, text/csv for Sheets,
        application/pdf for Slides) unless export_mime is provided.
        """
        service = self._build_service()
        # get basic metadata to decide method
        meta = service.files().get(fileId=file_id, fields='id, name, mimeType').execute()
        mime = meta.get('mimeType')
        name = meta.get('name')

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
                out_mime = export_mime or 'text/plain'
            request = service.files().export_media(fileId=file_id, mimeType=out_mime)
            return request, name, out_mime
        else:
            # regular file: download binary
            request = service.files().get_media(fileId=file_id)
            return request, name, mime

    def download_file_content(self, file_id: str, export_mime: Optional[str] = None) -> tuple[bytes, str]:
        """Download a file's content from Drive.

        Returns (bytes_content, filename).
        For Google Docs/Sheets/Slides this will export to a sensible textual format by default
        (text/plain for Docs, text/csv for Sheets, application/pdf for Slides) unless an
        explicit export_mime is provided.
        """
        service = self._build_service()
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