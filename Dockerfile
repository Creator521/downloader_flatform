# Use official lightweight Python image
FROM python:3.9-slim

# Install system dependencies (ffmpeg is required for yt-dlp audio conversion if needed, though we stream raw mostly)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose port (FastAPI default)
EXPOSE 8000

# Run the application with Gunicorn for production
# Workers = 4 usually good for general use, or 2*CPU+1
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "app.main:app", "--bind", "0.0.0.0:8000"]
