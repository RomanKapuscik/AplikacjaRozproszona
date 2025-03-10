from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import hashlib

app = FastAPI()

url_db = {}

class URLRequest(BaseModel):
    url: str

def generate_hash(url: str) -> str:
    """Create an 8 character hash for URL."""
    return hashlib.sha256(url.encode()).hexdigest()[:8]

@app.post("/shorten")
def shorten_url(request: URLRequest):
    """Shorten URL and save it in db (dict)."""
    url_hash = generate_hash(request.url)
    url_db[url_hash] = request.url
    return {"short_url": url_hash}

@app.get("/expand/{url_hash}")
def expand_url(url_hash: str):
    """Return full URL form hash."""
    if url_hash not in url_db:
        raise HTTPException(status_code=404, detail="URL not found")
    return {"original_url": url_db[url_hash]}

