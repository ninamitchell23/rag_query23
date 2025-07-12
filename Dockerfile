# Use Python base image
FROM python:3.10-slim

# Update system packages to reduce vulnerabilities and remove unnecessary packages
RUN apt-get update && apt-get upgrade -y && apt-get autoremove -y && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app/rag_app.py", "--server.port=8501", "--server.enableCORS=false"]
