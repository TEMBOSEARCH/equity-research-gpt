from sqlalchemy import Column, Integer, String, Date, ForeignKey, Text, UniqueConstraint
from sqlalchemy.orm import relationship
from db import Base

class Company(Base):
    __tablename__ = "companies"
    id = Column(Integer, primary_key=True)
    name = Column(String, index=True, nullable=False)
    country = Column(String, default="DE")
    filings = relationship("Filing", back_populates="company")

class Filing(Base):
    __tablename__ = "filings"
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    source = Column(String, nullable=False)
    filing_type = Column(String)
    filing_date = Column(Date)
    url = Column(Text)
    title = Column(Text)
    ext_id = Column(String)  # externe ID (z. B. North Data)
    company = relationship("Company", back_populates="filings")
    __table_args__ = (UniqueConstraint("source","ext_id", name="uq_source_extid"),)
