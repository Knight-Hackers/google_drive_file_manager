from fastapi import APIRouter, Header, HTTPException
from schemas.file_schemas import AnalysisSummary
from services.drive_service import get_drive_service, list_files
from services.categorize import categorize_files

router = APIRouter()

# list all .docx files
@router.get("/list")
def list_files(authorization: str = Header(...)):
    token = authorization.replace("Bearer ", "")
    service = get_drive_service(token)
    files = list_files(service)
    return {"files": files}

# categorize and analyze files (Heuristic-based)
@router.post("/analyze", response_model=AnalysisSummary)
def analyze_files(authorization: str = Header(...)):
    token = authorization.replace("Bearer ", "")
    service = get_drive_service(token)
    files = list_docx_files(service)
    result = categorize_files(files)
    return result

# endpoint 