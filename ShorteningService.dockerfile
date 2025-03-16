FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY shorten_api.py shorten_api.py

CMD ["uvicorn", "shorten_api:app", "--host", "0.0.0.0", "--port", "8000"]