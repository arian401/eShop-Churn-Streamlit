# syntax=docker/dockerfile:1

FROM python:3.11-slim

# System packages needed for building some Python wheels
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
&& rm -rf /var/lib/apt/lists/*

# Where our app lives in the container
WORKDIR /app

# Install Python dependencies first (leverages Docker layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the source
COPY . .

# Port FastAPI / Uvicorn will listen on
ENV PORT=10000

# Start the API
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]
