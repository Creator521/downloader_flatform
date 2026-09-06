FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    curl \
    unzip \
    && curl -fsSL https://deno.land/install.sh | DENO_INSTALL=/usr/local sh \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Create non-root user and set ownership
RUN useradd -r -s /bin/false appuser && chown -R appuser:appuser /app /tmp
USER appuser

# Expose port (FastAPI default)
EXPOSE 8000

# Run the application with Gunicorn for production
# Workers = 4 usually good for general use, or 2*CPU+1
CMD gunicorn -w ${WORKERS:-4} -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000
