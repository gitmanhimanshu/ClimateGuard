# Dockerfile for ClimateGuard AI
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements first (for caching)
COPY requirements.txt .
COPY pyproject.toml .
COPY uv.lock .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all application files
COPY models.py .
COPY openenv.yaml .
COPY inference.py .
COPY server/ ./server/
COPY static/ ./static/

# Expose port
EXPOSE 7860

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV ENABLE_WEB_INTERFACE=true

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:7860/health')"

# Run server
CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "7860"]
