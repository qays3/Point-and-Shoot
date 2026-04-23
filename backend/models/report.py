from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, JSON
from sqlalchemy.sql import func
from db.database import Base

class Report(Base):
    __tablename__ = "reports"

    id          = Column(Integer, primary_key=True, index=True)
    scan_id     = Column(Integer, ForeignKey("scans.id"), nullable=False, unique=True)
    target      = Column(String, nullable=False)
    duration    = Column(String, nullable=True)
    stats       = Column(JSON, default=dict)
    created_at  = Column(DateTime(timezone=True), server_default=func.now())