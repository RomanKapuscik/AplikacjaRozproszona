from fastapi import FastAPI
from pydantic import BaseModel, field_validator
from sqlalchemy import Column, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import hashlib, os

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db/url_db")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class URL(Base):
    __tablename__ = "urls"
    hash = Column(String, primary_key=True, index=True)
    original_url = Column(String, nullable=False)

Base.metadata.create_all(bind=engine)

app = FastAPI()

class URLRequest(BaseModel):
    url: str

    @field_validator("url", mode="before")
    @classmethod
    def validate_url(cls, url: str) -> str:
        if not url.startswith(("http://", "https://")):
            raise ValueError("URL musi zaczynać się od http:// lub https://")
        return url

def generate_hash(url: str) -> str:
    return hashlib.sha256(url.encode()).hexdigest()[:8]

@app.post("/shorten")
def shorten_url(request: URLRequest):
    """Shorten URL and save it in db."""
    db = SessionLocal()
    url_hash = generate_hash(str(request.url))
    db_url = db.query(URL).filter(URL.hash == url_hash).first()
    if not db_url:
        db_url = URL(hash=url_hash, original_url=request.url)
        db.add(db_url)
        db.commit()
    db.close()
    return {"short_url": url_hash}