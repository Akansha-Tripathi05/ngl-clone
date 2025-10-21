# Use an official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Optional: install curl/ping for debugging
RUN apt-get update && \
    apt-get install -y iputils-ping curl netcat-openbsd && \
    rm -rf /var/lib/apt/lists/*

# Set environment variables (optional)
ENV PYTHONUNBUFFERED=1

# Command to run your script
CMD ["python", "init_db.py"]
