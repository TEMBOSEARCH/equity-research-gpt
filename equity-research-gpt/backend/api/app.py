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


