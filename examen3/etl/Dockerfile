FROM python:3.9-slim

WORKDIR /app

COPY etl.py .
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "etl.py"]
