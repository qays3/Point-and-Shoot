from sqlalchemy import Column, Integer, String, DateTime, JSON, Enum
from sqlalchemy.sql import func
from db.database import Base
import enum

class ScanStatus(str, enum.Enum):
    pending = "pending"
    running = "running"
    done    = "done"
    error   = "error"

class Scan(Base):
    __tablename__ = "scans"

    id           = Column(Integer, primary_key=True, index=True)
    target       = Column(String, nullable=False)
    status       = Column(Enum(ScanStatus), default=ScanStatus.pending)
    engines      = Column(JSON, default=list)
    started_at   = Column(DateTime(timezone=True), server_default=func.now())
    finished_at  = Column(DateTime(timezone=True), nullable=True)