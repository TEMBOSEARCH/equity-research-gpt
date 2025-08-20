from fastapi import FastAPI, Depends, Query, HTTPException
from sqlalchemy import select, or_
from sqlalchemy.orm import Session
from typing import List, Optional

import db
from db import Base, engine, get_db
from models import Company, Filing
from schemas import CompanyOut, FilingOut

app = FastAPI(title="Equity Research API")

# Tabellen anlegen (einfacher Start – später gern mit Alembic)
Base.metadata.create_all(bind=engine)

@app.get("/healthz")
def healthz():
    return {"status": "ok"}

@app.get("/companies", response_model=List[CompanyOut])
def list_companies(
    q: Optional[str] = Query(None, description="Name enthält"),
    country: Optional[str] = None,
    dbs: Session = Depends(get_db)
):
    stmt = select(Company)
    if q:
        stmt = stmt.where(Company.name.ilike(f"%{q}%"))
    if country:
        stmt = stmt.where(Company.country == country)
    return dbs.execute(stmt.limit(200)).scalars().all()

@app.get("/filings", response_model=List[FilingOut])
def list_filings(
    q: Optional[str] = Query(None, description="Titel enthält"),
    dbs: Session = Depends(get_db)
):
    stmt = select(Filing)
    if q:
        stmt = stmt.where(Filing.title.ilike(f"%{q}%"))
    return dbs.execute(stmt.limit(200)).scalars().all()
