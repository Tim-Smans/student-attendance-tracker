FROM python:3.11-slim

WORKDIR /app

# Copy app files
COPY exporter.py .
COPY config.py .
COPY .env .

# Install dependencies
RUN pip install prometheus_client requests python-dotenv

# Expose port for Prometheus scraping
EXPOSE 8000

CMD ["python", "exporter.py"]
