FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN python -m pip install --no-cache-dir -r /app/requirements.txt

COPY ingestion /app/ingestion

# Default is a no-op container; run ingestion commands with `docker compose run worker ...`
CMD ["python", "-c", "print('worker container ready; run an ingestion command with docker compose run worker ...')"]

