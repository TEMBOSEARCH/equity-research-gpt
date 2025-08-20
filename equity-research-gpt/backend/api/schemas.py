from pydantic import BaseModel
from typing import Optional
from datetime import date

class CompanyOut(BaseModel):
    id: int
    name: str
    country: Optional[str]
    class Config:
        from_attributes = True

class FilingOut(BaseModel):
    id: int
    company_id: int
    source: str
    filing_type: Optional[str]
    filing_date: Optional[date]
    url: Optional[str]
    title: Optional[str]
    class Config:
        from_attributes = True
