from pydantic import BaseModel
from typing import Optional

class FindingResponse(BaseModel):
    id: int
    scan_id: int
    severity: str
    title: str
    engine: str
    description: Optional[str]
    url: Optional[str]
    method: Optional[str]
    remediation: Optional[str]

    class Config:
        from_attributes = True