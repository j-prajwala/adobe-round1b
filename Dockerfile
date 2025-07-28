# Use a slim Python image
FROM --platform=linux/amd64 python:3.10-slim

WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source and all necessary files
COPY . .

# Default command
CMD ["python", "run.py"]
