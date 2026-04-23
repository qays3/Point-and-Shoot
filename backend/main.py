from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path

from db.database import Base, engine
import models.scan
import models.finding
import models.report
from routers import scan, report, ws

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Point-and-Shoot", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(scan.router)
app.include_router(report.router)
app.include_router(ws.router)

BASE = Path(__file__).parent.parent

app.mount("/assets", StaticFiles(directory=BASE / "assets"), name="assets")

@app.get("/")
def index():
    return FileResponse(BASE / "index.html")

@app.get("/dashboard")
def dashboard():
    return FileResponse(BASE / "dashboard.html")

@app.get("/report")
def report_page():
    return FileResponse(BASE / "report.html")