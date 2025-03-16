FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY expand_api.py expand_api.py

CMD ["uvicorn", "expand_api:app", "--host", "0.0.0.0", "--port", "8001"]