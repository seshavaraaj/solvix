FROM python:3.12-slim

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
# Seed is idempotent: it reloads the flood layer and only adds synthetic reports when none exist.
CMD ["sh", "-c", "python -m seed.seed && uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
