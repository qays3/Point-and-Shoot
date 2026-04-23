from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ScanCreate(BaseModel):
    target: str
    engines: List[str] = [
        "subdomain","pulse","dns","xray",
        "idor","dirfinder","secrets","cors","headers"
    ]

class ScanResponse(BaseModel):
    id: int
    target: str
    status: str
    engines: List[str]
    started_at: Optional[datetime]
    finished_at: Optional[datetime]

    class Config:
        from_attributes = True