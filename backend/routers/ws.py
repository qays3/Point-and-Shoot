from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from models.scan import Scan, ScanStatus
from services.orchestrator import run_scan
import json

router = APIRouter(tags=["websocket"])

@router.websocket("/ws/scan/{scan_id}")
async def websocket_scan(scan_id: int, ws: WebSocket, db: Session = Depends(get_db)):
    await ws.accept()

    scan = db.query(Scan).filter(Scan.id == scan_id).first()
    if not scan:
        await ws.send_text(json.dumps({"type": "error", "message": "Scan not found"}))
        await ws.close()
        return

    if scan.status not in [ScanStatus.pending, ScanStatus.running]:
        await ws.send_text(json.dumps({"type": "error", "message": "Scan already completed"}))
        await ws.close()
        return

    try:
        await run_scan(scan, db, ws)
    except WebSocketDisconnect:
        pass
    finally:
        try:
            await ws.close()
        except Exception:
            pass