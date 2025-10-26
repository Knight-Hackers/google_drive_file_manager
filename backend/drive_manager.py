
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os
import pickle
from typing import Dict, List, Optional
import hashlib

class DriveManager:
    """A class to manage Google Drive operations including file organization and duplicate detection."""
    
    SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
    
    def __init__(self, credentials_path: str, token_path: str):
        """
        Initialize the DriveManager.
        
        Args:
            credentials_path (str): Path to the credentials.json file
            token_path (str): Path to save/load the token.pickle file
        """
        self.credentials_path = credentials_path
        self.token_path = token_path
        self.service = self._authenticate()
        
    def _authenticate(self) -> any:
        """Authenticate with Google Drive API."""
        creds = None
        
        if os.path.exists(self.token_path):
            with open(self.token_path, 'rb') as token:
                creds = pickle.load(token)
                
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, self.SCOPES)
                creds = flow.run_local_server(port=0)
                
            with open(self.token_path, 'wb') as token:
                pickle.dump(creds, token)
                
        return build('drive', 'v3', credentials=creds)
    
    def list_all_files(self, folder_id: Optional[str] = None) -> List[Dict]:
        """
        List all files in the drive or in a specific folder.
        
        Args:
            folder_id (str, optional): ID of the folder to list files from.
                                     If None, lists files from root.
                                     
        Returns:
            List[Dict]: List of dictionaries containing file information
        """
        results = []
        page_token = None
        
        while True:
            query = "trashed = false"
            if folder_id:
                query += f" and '{folder_id}' in parents"
                
            response = self.service.files().list(
                q=query,
                spaces='drive',
                fields='nextPageToken, files(id, name, mimeType, parents, md5Checksum, size)',
                pageToken=page_token
            ).execute()
            
            results.extend(response.get('files', []))
            page_token = response.get('nextPageToken')
            
            if not page_token:
                break
                
        return results
    
    def find_file_by_name(self, file_name: str) -> List[Dict]:
        """
        Find files by name.
        
        Args:
            file_name (str): Name of the file to search for
            
        Returns:
            List[Dict]: List of dictionaries containing file information
        """
        query = f"name contains '{file_name}' and trashed = false"
        response = self.service.files().list(
            q=query,
            spaces='drive',
            fields='files(id, name, mimeType, parents)'
        ).execute()
        
        return response.get('files', [])
    
    def detect_duplicates(self) -> Dict[str, List[Dict]]:
        """
        Detect duplicate files based on MD5 checksums.
        
        Returns:
            Dict[str, List[Dict]]: Dictionary mapping MD5 checksums to lists of duplicate files
        """
        all_files = self.list_all_files()
        checksum_map: Dict[str, List[Dict]] = {}
        
        for file in all_files:
            if 'md5Checksum' in file:
                checksum = file['md5Checksum']
                if checksum in checksum_map:
                    checksum_map[checksum].append(file)
                else:
                    checksum_map[checksum] = [file]
        
        # Filter out files that don't have duplicates
        return {k: v for k, v in checksum_map.items() if len(v) > 1}
    
    def get_file_metadata(self, file_id: str) -> Dict:
        """
        Get detailed metadata for a specific file.
        
        Args:
            file_id (str): ID of the file
            
        Returns:
            Dict: Dictionary containing file metadata
        """
        return self.service.files().get(
            fileId=file_id,
            fields='id, name, mimeType, parents, md5Checksum, size, createdTime, modifiedTime'
        ).execute()
    
    def get_folder_structure(self, folder_id: Optional[str] = None) -> Dict:
        """
        Get the folder structure starting from a specific folder or root.
        
        Args:
            folder_id (str, optional): ID of the starting folder. If None, starts from root.
            
        Returns:
            Dict: Dictionary representing the folder structure
        """
        def build_tree(current_id: Optional[str]) -> Dict:
            query = f"'{current_id}' in parents" if current_id else "root in parents"
            query += " and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
            
            response = self.service.files().list(
                q=query,
                spaces='drive',
                fields='files(id, name)'
            ).execute()
            
            tree = {}
            for folder in response.get('files', []):
                tree[folder['name']] = build_tree(folder['id'])
            return tree
            
        return build_tree(folder_id)