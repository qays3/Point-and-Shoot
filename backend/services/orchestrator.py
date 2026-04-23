import asyncio
import json
from fastapi import WebSocket
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from models.scan import Scan, ScanStatus
from models.finding import Finding
from services import subdomain, pulse, dns_investigator, xray, idor, dir_finder, secret_sniffer, cors_interrogator, header_analyzer

ENGINE_MAP = {
    "subdomain":  subdomain,
    "pulse":      pulse,
    "dns":        dns_investigator,
    "xray":       xray,
    "idor":       idor,
    "dirfinder":  dir_finder,
    "secrets":    secret_sniffer,
    "cors":       cors_interrogator,
    "headers":    header_analyzer,
}

async def run_scan(scan: Scan, db: Session, ws: WebSocket):
    engines = [e for e in scan.engines if e in ENGINE_MAP]
    total = len(engines)
    done = 0

    await _send(ws, {"type": "status", "engine": None, "status": "running"})

    scan.status = ScanStatus.running
    db.commit()

    for engine_key in engines:
        await _send(ws, {"type": "engine", "engine": engine_key, "status": "running"})

        try:
            result = await ENGINE_MAP[engine_key].run(scan.target)
        except Exception as e:
            await _send(ws, {"type": "log", "log": {"type": "warn", "text": f"[!] {engine_key} crashed: {str(e)}"}})
            await _send(ws, {"type": "engine", "engine": engine_key, "status": "error"})
            done += 1
            continue

        for log in result.get("logs", []):
            await _send(ws, {"type": "log", "log": log})

        for f in result.get("findings", []):
            finding = Finding(
                scan_id=scan.id,
                severity=f["severity"],
                title=f["title"],
                engine=f["engine"],
                description=f.get("description"),
                url=f.get("url"),
                method=f.get("method"),
                remediation=f.get("remediation"),
            )
            db.add(finding)
            db.commit()
            db.refresh(finding)
            await _send(ws, {"type": "finding", "finding": {
                "id": finding.id,
                "severity": finding.severity,
                "title": finding.title,
                "engine": finding.engine,
                "description": finding.description,
                "url": finding.url,
                "method": finding.method,
                "remediation": finding.remediation,
            }})

        done += 1
        pct = round((done / total) * 100)
        await _send(ws, {"type": "engine",   "engine": engine_key, "status": "done"})
        await _send(ws, {"type": "progress", "pct": pct, "label": f"{engine_key.upper()} complete"})

    scan.status = ScanStatus.done
    scan.finished_at = datetime.now(timezone.utc)
    db.commit()

    await _send(ws, {"type": "status", "engine": None, "status": "done"})
    await _send(ws, {"type": "log",    "log": {"type": "info", "text": "[+] Scan complete. View full report in the Report tab."}})

async def _send(ws: WebSocket, data: dict):
    try:
        await ws.send_text(json.dumps(data))
    except Exception:
        pass