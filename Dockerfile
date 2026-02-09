FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY migrate_to_mongo.py .

CMD ["python", "migrate_to_mongo.py"]
