from pydantic import BaseModel
from typing import List, Optional, Dict

class FileMetadata(BaseModel):
    id: str
    name: str
    mime_type: str
    size: Optional[int]
    modifiedTime: Optional[str]

class CategorizedFile(BaseModel):
    name: str
    category: str
    confidence: Optional[float]=None

class AnalysisSummary(BaseModel):
    total_files: int
    categories: Dict[str, int]
    files: List[CategorizedFile]