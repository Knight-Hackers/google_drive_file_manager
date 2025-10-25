from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

access_token = "ya29.a0ATi6K2vrEjs6bgRpYAeerRka2fENXmHtehExpz5rOfYfVm9uNGyh4LmaY0Q5jZnVw44BNECiTSLEa4jWnJIUQrsWNx_QnaJTyUOTDEby5_RzV2k8ZAM_DEolwE2Y1tpySGpOVJA93zF2z3_3qw1WvbTWtzQdQP-dIHT11QzfGvAC0N_OAmDwO-TT7zKa5FxygZKITUkaCgYKAaMSARUSFQHGX2MiNIbfYR0hg2pGqe4PaRkZ1g0206"
# retrieve all .docx files from Drive
def get_drive_service(access_token: str):
    creds = Credentials(token=access_token)
    service = build('drive', 'v3', credentials=creds)
    return service

# list .docx files
def list_files(service):
    results = service.files().list(
        q="mimeType='application/vnd.openxmlformats-officedocument.wordprocessingml.document'",
        fields = "files(id, name, mimeType, modifiedTime, size)"
    ).execute()
    return results.get('files', [])