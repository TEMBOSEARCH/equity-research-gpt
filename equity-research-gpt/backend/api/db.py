import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Wenn DATABASE_URL (Neon) nicht gesetzt ist, läuft es lokal mit SQLite.
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///equity.db")

engine = create_engine(DATABASE_URL, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
