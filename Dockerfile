FROM python:3.10.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# Run Gunicorn
CMD ["gunicorn", "--workers=2", "--threads=2", "--bind", "0.0.0.0:8000", "app:app"]