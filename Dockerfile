FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# Bind to the port provided by the host ($PORT on Render/Railway), default to 8000 locally.
# Shell form is required so ${PORT} is expanded at runtime.
CMD uvicorn api.main:app --host 0.0.0.0 --port ${PORT:-8000}
