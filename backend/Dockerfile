# Backend Dockerfile for FastAPI + Chainlit demo
FROM python:3.11-slim

WORKDIR /app

# system deps
RUN apt-get update && apt-get install -y build-essential git curl && rm -rf /var/lib/apt/lists/*

# copy only requirements first for efficient caching
COPY backend/requirements.txt /app/requirements.txt
RUN python -m pip install --upgrade pip setuptools wheel
RUN python -m pip install -r /app/requirements.txt

# copy app code
COPY backend /app/backend

ENV PYTHONUNBUFFERED=1
ENV BACKEND_PORT=8000
ENV CHAINLIT_PORT=8001

EXPOSE 8000 8001

# Default command: start uvicorn
CMD ["python", "-m", "uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
