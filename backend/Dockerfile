FROM python:3.9-slim

WORKDIR /app
COPY . .


# Install netcat-openbsd instead of netcat
RUN apt-get update && apt-get install -y netcat-openbsd gcc libpq-dev && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir gunicorn && \
    apt-get clean && rm -rf /var/lib/apt/lists/*


# Expose port
EXPOSE 5000

# Use entrypoint script to wait for DB
ENTRYPOINT ["./wait-for-db.sh"]

