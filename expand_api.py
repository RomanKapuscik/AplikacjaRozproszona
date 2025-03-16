from fastapi import FastAPI, HTTPException
from sqlalchemy import Column, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db/url_db")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# URL model
class URL(Base):
    __tablename__ = "urls"
    hash = Column(String, primary_key=True, index=True)
    original_url = Column(String, nullable=False)

# Create tables
Base.metadata.create_all(bind=engine)

# FastAPI app
app = FastAPI()

@app.get("/expand/{url_hash}")
def expand_url(url_hash: str):
    """Return full URL from hash."""
    db = SessionLocal()
    db_url = db.query(URL).filter(URL.hash == url_hash).first()
    db.close()
    if not db_url:
        raise HTTPException(status_code=404, detail="URL not found")
    return {"original_url": db_url.original_url}