from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from models.scan import Scan, ScanStatus
from schemas.scan import ScanCreate, ScanResponse

router = APIRouter(prefix="/api/scan", tags=["scan"])

@router.post("", response_model=ScanResponse)
def create_scan(body: ScanCreate, db: Session = Depends(get_db)):
    scan = Scan(target=body.target, engines=body.engines, status=ScanStatus.pending)
    db.add(scan)
    db.commit()
    db.refresh(scan)
    return scan

@router.get("/{scan_id}", response_model=ScanResponse)
def get_scan(scan_id: int, db: Session = Depends(get_db)):
    scan = db.query(Scan).filter(Scan.id == scan_id).first()
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    return scan

@router.get("", response_model=list[ScanResponse])
def list_scans(db: Session = Depends(get_db)):
    return db.query(Scan).order_by(Scan.id.desc()).limit(20).all()