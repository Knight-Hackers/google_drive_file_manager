from dotenv import load_dotenv
import os
from .BaseTool import BaseTool
from typing import Dict, Any, List, Optional
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build


load_dotenv()

class FileManager(BaseTool):

    """
    Agent that gathers cloud/drive data
    Helper tool for gemini so that it can organize files based on properties
    (e.g. name, size, date, contents).
    """

    def __init__(self, name):
        super().__init__(name=name, description="Drive file manager tool", supported_file_types=None)
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
        """Create a Google Drive service using a service account (preferred).

        Supports either a path to a JSON key file (GOOGLE_SERVICE_ACCOUNT_PATH)
        or a raw JSON string in GOOGLE_SERVICE_ACCOUNT_JSON.
        """
        if self._service:
            return self._service

        creds = None
        if self.service_account_path and os.path.exists(self.service_account_path):
            creds = service_account.Credentials.from_service_account_file(self.service_account_path, scopes=self.scopes)
        elif self.service_account_json:
            try:
                info = json.loads(self.service_account_json)
                creds = service_account.Credentials.from_service_account_info(info, scopes=self.scopes)
            except Exception as e:
                raise RuntimeError(f"Failed to parse GOOGLE_SERVICE_ACCOUNT_JSON: {e}")
        else:
            raise RuntimeError("No service account configured. Set GOOGLE_SERVICE_ACCOUNT_PATH or GOOGLE_SERVICE_ACCOUNT_JSON in environment.")

        self._service = build('drive', 'v3', credentials=creds)
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

        service = self._build_service()

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