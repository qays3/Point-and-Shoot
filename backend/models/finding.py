from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from db.database import Base
import enum

class Severity(str, enum.Enum):
    high = "high"
    med  = "med"
    low  = "low"

class Finding(Base):
    __tablename__ = "findings"

    id          = Column(Integer, primary_key=True, index=True)
    scan_id     = Column(Integer, ForeignKey("scans.id"), nullable=False)
    severity    = Column(Enum(Severity), nullable=False)
    title       = Column(String, nullable=False)
    engine      = Column(String, nullable=False)
    description = Column(String, nullable=True)
    url         = Column(String, nullable=True)
    method      = Column(String, nullable=True)
    remediation = Column(String, nullable=True)