from fastapi import FastAPI, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import List, Optional

import db
from db import Base, engine, get_db
from models import Company, Filing
from schemas import CompanyOut, FilingOut

app = FastAPI(title="Equity Research API")
Base.metadata.create_all(bind=engine)
# --- Crawler-Trigger (statt Render-Cron) ---
import os, sys
from fastapi import HTTPException

# Pfad so setzen, dass 'crawler.providers.northdata' importierbar ist
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from crawler.providers.northdata import run_delta  # <- WICHTIG: mit 'crawler.' Präfix

RUN_TOKEN = os.getenv("RUN_TOKEN")

@app.post("/admin/run-crawler")
def run_crawler(limit: int = 20, token: str | None = None):
    if RUN_TOKEN and token != RUN_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")
    run_delta(limit=limit)
    return {"status": "crawler_ok", "limit": limit}
