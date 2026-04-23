from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from models.scan import Scan
from models.finding import Finding
from schemas.report import ReportResponse
from schemas.finding import FindingResponse

router = APIRouter(prefix="/api/report", tags=["report"])

@router.get("/{scan_id}", response_model=ReportResponse)
def get_report(scan_id: int, db: Session = Depends(get_db)):
    scan = db.query(Scan).filter(Scan.id == scan_id).first()
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")

    findings = db.query(Finding).filter(Finding.scan_id == scan_id).all()

    duration = None
    if scan.started_at and scan.finished_at:
        delta = (scan.finished_at - scan.started_at).total_seconds()
        s = int(delta)
        duration = f"{s // 60}m {s % 60}s" if s >= 60 else f"{s}s"

    stats = {
        "total": len(findings),
        "high":  sum(1 for f in findings if f.severity == "high"),
        "med":   sum(1 for f in findings if f.severity == "med"),
        "low":   sum(1 for f in findings if f.severity == "low"),
        "engines": len(scan.engines) if scan.engines else 0,
    }

    return ReportResponse(
        scan_id=scan.id,
        target=scan.target,
        status=scan.status,
        started_at=scan.started_at.isoformat() if scan.started_at else None,
        finished_at=scan.finished_at.isoformat() if scan.finished_at else None,
        duration=duration,
        findings=[FindingResponse.model_validate(f) for f in findings],
        stats=stats,
    )