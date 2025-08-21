# app.py (Ausschnitt – so am Anfang)
from fastapi import FastAPI, Depends, Query, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import Optional, List

from db import Base, engine, get_db
from models import Company, Filing
from schemas import CompanyOut, FilingOut

app = FastAPI(title="Equity Research API")
Base.metadata.create_all(bind=engine)

# --- Healthcheck (muss laufen) ---
@app.get("/healthz")
def healthz():
    return {"status": "ok"}

# --- Crawler-Trigger (Import erst beim Aufruf, damit Start nie crasht) ---
import os, sys
RUN_TOKEN = os.getenv("RUN_TOKEN")

@app.post("/admin/run-crawler")
def run_crawler(limit: int = 20, token: Optional[str] = None):
    if RUN_TOKEN and token != RUN_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # Pfad so setzen, dass 'crawler.providers.northdata' gefunden wird
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    if BASE_DIR not in sys.path:
        sys.path.insert(0, BASE_DIR)

    try:
        from crawler.providers.northdata import run_delta
    except Exception as e:
        # klare Fehlermeldung statt App-Crash
        raise HTTPException(status_code=500, detail=f"Could not import crawler: {e}")

    # Crawler ausführen
    run_delta(limit=limit)
    return {"status": "crawler_ok", "limit": limit}
