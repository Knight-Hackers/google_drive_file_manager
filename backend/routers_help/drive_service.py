from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build


# retrieve all .docx files from Drive
def get_drive_service(access_token: str):
    creds = Credentials(token=access_token) # convert token into credentials object
    service = build('drive', 'v3', credentials=creds) # initiate google drive api client 
    return service # able to query drive with this service object

# list .docx files
def list_files(service):
    results = service.files().list(
        q="mimeType='application/vnd.google-apps.document' and trashed=false", # query for searching files within the drive
        fields = "files(id, name, mimeType, modifiedTime, size)" # fields to return from each file
    ).execute()
    return results.get('files', []) 