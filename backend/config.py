from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv(Path(__file__).parent / ".env")

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./pointshoot.db")
BASE_DIR = Path(__file__).parent.parent