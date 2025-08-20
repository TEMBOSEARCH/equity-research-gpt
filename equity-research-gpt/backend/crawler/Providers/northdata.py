from datetime import datetime
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..db import engine, SessionLocal, Base
from ..models import Company, Filing
from .northdata_client import NorthDataClient

def _upsert_company(dbs: Session, name: str) -> int:
    row = dbs.execute(select(Company).where(Company.name == name)).scalar_one_or_none()
    if row:
        return row.id
    obj = Company(name=name, country="DE")
    dbs.add(obj); dbs.commit(); dbs.refresh(obj)
    return obj.id

def _save_pub(dbs: Session, company_id: int, p: dict):
    ext_id = str(p.get("id") or p.get("publicationId") or "")
    title = p.get("title") or p.get("subject") or ""
    url = p.get("url") or p.get("link") or None
    date_str = p.get("publicationDate") or p.get("timestamp")
    filing_date = None
    if date_str:
        filing_date = datetime.fromisoformat(date_str.replace("Z","+00:00")).date()

    # Duplikate anhand (source, ext_id) vermeiden:
    exists = dbs.execute(select(Filing).where(Filing.source=="northdata", Filing.ext_id==ext_id)).scalar_one_or_none()
    if exists:
        return

    f = Filing(
        company_id=company_id,
        source="northdata",
        filing_type=p.get("topic") or p.get("topicType"),
        filing_date=filing_date,
        url=url,
        title=title,
        ext_id=ext_id
    )
    dbs.add(f); dbs.commit()

def run_delta(limit: int = 20):
    Base.metadata.create_all(bind=engine)
    cli = NorthDataClient()
    with SessionLocal() as dbs:
        res = cli.publications(limit=limit, source="bundesanzeiger")
        items = res.get("publications") or res.get("items") or []
        for p in items:
            name = (p.get("publisher") or {}).get("name") or p.get("companyName") or "Unknown"
            cid = _upsert_company(dbs, name)
            _save_pub(dbs, cid, p)
