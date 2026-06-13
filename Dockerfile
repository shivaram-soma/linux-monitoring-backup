FROM python:3.11-slim

# psutil needs gcc for compilation on slim image
RUN apt-get update && apt-get install -y --no-install-recommends gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY monitor.py graph.py ./

# Output directory for logs and charts
RUN mkdir -p /app/output

# Default: continuous monitoring
CMD ["python3", "monitor.py", "--loop"]
