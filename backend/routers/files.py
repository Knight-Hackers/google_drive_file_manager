from fastapi import APIRouter, Header, HTTPException
from schemas.file_schemas import AnalysisSummary
from routers_help.drive_service import get_drive_service, list_files
from routers_help.categorize import categorize_files

router = APIRouter()

# list all google docs files
@router.get("/list")
def list_files_route(authorization: str = Header(...)): # function expects a header called Authorization in the HTTP request
    token = authorization.replace("Bearer ", "") # extract access token from header
    service = get_drive_service(token) # create drive client
    files = list_files(service) # extract metadate for all google docs files
    return {"files": files} # wrap metadate list into dictionary and return as a JSON response

# categorize and analyze files (Heuristic-based)
@router.post("/analyze", response_model=AnalysisSummary)
def analyze_files(authorization: str = Header(...)):
    token = authorization.replace("Bearer ", "")
    service = get_drive_service(token)
    files = list_files(service)
    result = categorize_files(files)
    return result