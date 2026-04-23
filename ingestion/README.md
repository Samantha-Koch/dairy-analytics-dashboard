# Ingestion

This folder contains scripts to ingest raw datasets into Postgres following `docs/canonical_schema.md`.

## Setup

1. Create an `.env` (copy from `.env.example`) and set `DATABASE_URL`.
2. Install dependencies (pick one):
   - `uv sync` (recommended)
   - or `pip install -r ..\\requirements.txt` (if you prefer pip; see repo root)

## Run

Ingest a USDA-style "long" CSV with columns like: `year, period, category, data_item, value, unit/units`.

```bash
python -m ingestion_py.ingest_usda_long_csv --dataset-slug usda_prod_factors --dataset-name "Milk production and factors affecting supply" --csv "C:\path\to\annual-milk-prod-factors.csv"
```

