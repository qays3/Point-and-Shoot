from pydantic import BaseModel
from typing import Optional, List
from schemas.finding import FindingResponse

class ReportResponse(BaseModel):
    scan_id: int
    target: str
    status: str
    started_at: Optional[str]
    finished_at: Optional[str]
    duration: Optional[str]
    findings: List[FindingResponse]
    stats: dict

class ReportSummary(BaseModel):
    scan_id: int
    target: str
    status: str
    total: int
    high: int
    med: int
    low: int
    duration: Optional[str]
    created_at: Optional[str]