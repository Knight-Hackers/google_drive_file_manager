from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# retrieve all .docx files from Drive
def get_drive_service(access_token: str):
    creds = Credentials(token=access_token)
    service = build('drive', 'v3', credentials=creds)
    return service

# list .docx files
def list_files(service):
    results = service.files().list(
        q="mimeType=application/vnd.openxmlformats-officedocument.wordprocessingml.document'",
        fields = "files(id, name, mimeType, modifiedTime, size)"
    ).execute()
    return results.get('files', [])