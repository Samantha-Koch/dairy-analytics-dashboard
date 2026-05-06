from __future__ import annotations

import argparse
import os
import uuid
from datetime import datetime, timezone
import json

import pandas as pd
from sqlalchemy import text

from ingestion_py.db import get_engine
from ingestion_py.schema import ensure_schema
from ingestion_py.usda_periods import parse_year_period


def _slugify_metric_part(s: str) -> str:
    return (
        str(s)
        .strip()
        .lower()
        .replace(" ", "_")
        .replace("-", "_")
        .replace("/", "_")
    )


def _pick_col(df: pd.DataFrame, *candidates: str) -> str | None:
    for c in candidates:
        if c in df.columns:
            return c
    return None


def main() -> None:
    parser = argparse.ArgumentParser(description="Ingest a USDA-style long CSV into canonical tables.")
    parser.add_argument("--dataset-slug", required=True, help="Unique dataset slug, e.g. usda_prod_factors")
    parser.add_argument("--dataset-name", required=True, help="Human dataset name")
    parser.add_argument("--dataset-type", default="usda", choices=["usda", "user_upload"])
    parser.add_argument("--provider", default="USDA")
    parser.add_argument("--csv", required=True, help="Path to CSV file")
    parser.add_argument("--raw-uri", default=None)
    args = parser.parse_args()

    csv_path = args.csv
    if not os.path.exists(csv_path):
        raise FileNotFoundError(csv_path)

    engine = get_engine()
    ensure_schema(engine)

    df = pd.read_csv(csv_path, encoding="latin1")
    df.columns = [c.strip().lower() for c in df.columns]

    year_col = _pick_col(df, "year")
    period_col = _pick_col(df, "period")
    category_col = _pick_col(df, "category")
    data_item_col = _pick_col(df, "data_item", "dataitem", "item")
    value_col = _pick_col(df, "value")
    unit_col = _pick_col(df, "unit", "units")

    required = {"year": year_col, "data_item": data_item_col, "value": value_col}
    missing = [k for k, v in required.items() if v is None]
    if missing:
        raise ValueError(f"CSV missing required columns: {missing}. Found columns={list(df.columns)}")

    df = df.copy()
    df["year"] = pd.to_numeric(df[year_col], errors="raise").astype(int)
    df["period_raw"] = df[period_col] if period_col else "annual"
    df["category_raw"] = df[category_col] if category_col else None
    df["data_item_raw"] = df[data_item_col].astype(str)
    df["value"] = pd.to_numeric(df[value_col], errors="coerce")
    df["unit"] = df[unit_col].astype(str) if unit_col else None
    df = df[df["value"].notna()]

    now = datetime.now(tz=timezone.utc)
    run_id = uuid.uuid4()
    dataset_id = str(uuid.uuid5(uuid.NAMESPACE_URL, f"dataset:{args.dataset_slug}"))

    default_geo_id = os.environ.get("DEFAULT_GEO_ID", "US")
    default_entity_id = os.environ.get("DEFAULT_ENTITY_ID", "usda")

    # Build canonical periods
    periods = {}
    for y, p in df[["year", "period_raw"]].drop_duplicates().itertuples(index=False):
        cp = parse_year_period(int(y), None if pd.isna(p) else str(p))
        periods[cp.time_id] = cp

    # Build metrics and mapping
    metric_rows = []
    metric_map_rows = []

    # stable set: use the dataset_slug, plus optional category to avoid collisions
    for _, r in df[["category_raw", "data_item_raw"]].drop_duplicates().iterrows():
        cat = r["category_raw"]
        item = r["data_item_raw"]
        source_category = None if pd.isna(cat) else str(cat)
        source_item = str(item)
        cat_part = _slugify_metric_part(source_category) if source_category else None
        item_part = _slugify_metric_part(source_item)

        metric_id = (
            f"{args.dataset_slug}__{cat_part}__{item_part}" if cat_part else f"{args.dataset_slug}__{item_part}"
        )
        metric_rows.append(
            {
                "metric_id": metric_id,
                "name": source_item.replace("_", " ").title(),
                "allowed_period_types": ["year", "quarter", "month"],
                "description": None,
                "domain": None,
                "base_unit": None,
                "value_type": None,
                "aggregation": None,
            }
        )
        metric_map_rows.append(
            {
                "dataset_id": dataset_id,
                "source_category": source_category,
                "source_data_item": source_item,
                "metric_id": metric_id,
            }
        )

    # Deduplicate metric_rows on metric_id
    by_id = {}
    for r in metric_rows:
        by_id[r["metric_id"]] = r
    metric_rows = list(by_id.values())

    with engine.begin() as conn:
        # seed geo + entity
        conn.execute(
            text(
                """
                INSERT INTO dim_geo (geo_id, geo_level, scheme, code, name, parent_geo_id)
                VALUES (:geo_id, 'national', 'NATIONAL', NULL, 'United States', NULL)
                ON CONFLICT (geo_id) DO NOTHING;
                """
            ),
            {"geo_id": default_geo_id},
        )
        conn.execute(
            text(
                """
                INSERT INTO dim_entity (entity_id, entity_type, display_name, owner_user_id, default_geo_id)
                VALUES (:entity_id, 'usda', 'USDA', NULL, :geo_id)
                ON CONFLICT (entity_id) DO NOTHING;
                """
            ),
            {"entity_id": default_entity_id, "geo_id": default_geo_id},
        )

        # dataset + run
        conn.execute(
            text(
                """
                INSERT INTO dataset (dataset_id, dataset_slug, dataset_type, name, provider, refresh_cadence, raw_uri, notes)
                VALUES (:dataset_id, :dataset_slug, :dataset_type, :name, :provider, NULL, :raw_uri, NULL)
                ON CONFLICT (dataset_id) DO UPDATE
                SET dataset_slug=EXCLUDED.dataset_slug,
                    dataset_type=EXCLUDED.dataset_type,
                    name=EXCLUDED.name,
                    provider=EXCLUDED.provider,
                    raw_uri=EXCLUDED.raw_uri;
                """
            ),
            {
                "dataset_id": dataset_id,
                "dataset_slug": args.dataset_slug,
                "dataset_type": args.dataset_type,
                "name": args.dataset_name,
                "provider": args.provider,
                "raw_uri": args.raw_uri,
            },
        )
        conn.execute(
            text(
                """
                INSERT INTO dataset_run (run_id, dataset_id, status, started_at)
                VALUES (:run_id, :dataset_id, 'started', :started_at);
                """
            ),
            {"run_id": str(run_id), "dataset_id": dataset_id, "started_at": now},
        )

        # dim_time upsert
        for cp in periods.values():
            conn.execute(
                text(
                    """
                    INSERT INTO dim_time (time_id, period_type, year, quarter, month, period_start, period_end)
                    VALUES (:time_id, :period_type, :year, :quarter, :month, :period_start, :period_end)
                    ON CONFLICT (time_id) DO UPDATE
                    SET period_type=EXCLUDED.period_type,
                        year=EXCLUDED.year,
                        quarter=EXCLUDED.quarter,
                        month=EXCLUDED.month,
                        period_start=EXCLUDED.period_start,
                        period_end=EXCLUDED.period_end;
                    """
                ),
                {
                    "time_id": cp.time_id,
                    "period_type": cp.period_type,
                    "year": cp.year,
                    "quarter": cp.quarter,
                    "month": cp.month,
                    "period_start": cp.period_start,
                    "period_end": cp.period_end,
                },
            )

        # dim_metric upsert
        for r in metric_rows:
            conn.execute(
                text(
                    """
                    INSERT INTO dim_metric (metric_id, name, allowed_period_types, description, domain, base_unit, value_type, aggregation)
                    VALUES (:metric_id, :name, :allowed_period_types, :description, :domain, :base_unit, :value_type, :aggregation)
                    ON CONFLICT (metric_id) DO UPDATE
                    SET name=EXCLUDED.name,
                        allowed_period_types=EXCLUDED.allowed_period_types;
                    """
                ),
                r,
            )

        # metric_source_map upsert (conflict on PK)
        for r in metric_map_rows:
            conn.execute(
                text(
                    """
                    INSERT INTO metric_source_map (dataset_id, source_category, source_data_item, metric_id)
                    VALUES (:dataset_id, :source_category, :source_data_item, :metric_id)
                    ON CONFLICT (dataset_id, source_category, source_data_item) DO UPDATE
                    SET metric_id=EXCLUDED.metric_id;
                    """
                ),
                r,
            )

        # Build fact rows; derive metric_id consistently with the mapping convention above
        fact_rows = []
        for row in df.itertuples(index=False):
            y = int(getattr(row, "year"))
            period_raw = getattr(row, "period_raw")
            cat_raw = getattr(row, "category_raw")
            item_raw = getattr(row, "data_item_raw")
            value = float(getattr(row, "value"))
            unit = getattr(row, "unit") if "unit" in df.columns else None

            cp = parse_year_period(y, None if pd.isna(period_raw) else str(period_raw))
            source_category = None if pd.isna(cat_raw) else str(cat_raw)
            cat_part = _slugify_metric_part(source_category) if source_category else None
            item_part = _slugify_metric_part(str(item_raw))
            metric_id = (
                f"{args.dataset_slug}__{cat_part}__{item_part}" if cat_part else f"{args.dataset_slug}__{item_part}"
            )

            fact_rows.append(
                {
                    "observation_id": str(uuid.uuid4()),
                    "metric_id": metric_id,
                    "time_id": cp.time_id,
                    "geo_id": default_geo_id,
                    "entity_id": default_entity_id,
                    "value": value,
                    "unit": None if unit is None else str(unit),
                    "source": args.dataset_type,
                    "dataset_id": dataset_id,
                    "run_id": str(run_id),
                    "source_series_id": None,
                    "source_category": source_category,
                    "source_data_item": str(item_raw),
                    "source_period": None if pd.isna(period_raw) else str(period_raw),
                    "quality_flag": None,
                    "ingested_at": now,
                }
            )

        # Insert facts with upsert on natural unique key
        for r in fact_rows:
            conn.execute(
                text(
                    """
                    INSERT INTO fact_observation (
                        observation_id, metric_id, time_id, geo_id, entity_id, value, unit, source,
                        dataset_id, run_id, source_series_id, source_category, source_data_item, source_period,
                        quality_flag, ingested_at
                    )
                    VALUES (
                        :observation_id, :metric_id, :time_id, :geo_id, :entity_id, :value, :unit, :source,
                        :dataset_id, :run_id, :source_series_id, :source_category, :source_data_item, :source_period,
                        :quality_flag, :ingested_at
                    )
                    ON CONFLICT (metric_id, time_id, geo_id, entity_id) DO UPDATE
                    SET value=EXCLUDED.value,
                        unit=EXCLUDED.unit,
                        dataset_id=EXCLUDED.dataset_id,
                        run_id=EXCLUDED.run_id,
                        source_category=EXCLUDED.source_category,
                        source_data_item=EXCLUDED.source_data_item,
                        source_period=EXCLUDED.source_period,
                        ingested_at=EXCLUDED.ingested_at;
                    """
                ),
                r,
            )

        conn.execute(
            text(
                """
                UPDATE dataset_run
                SET status='succeeded', finished_at=:finished_at, stats_json=:stats_json
                WHERE run_id=:run_id;
                """
            ),
            {
                "run_id": str(run_id),
                "finished_at": datetime.now(tz=timezone.utc),
                "stats_json": json.dumps({"rows_ingested": int(len(fact_rows))}),
            },
        )

    print(f"Ingested {len(df)} rows into fact_observation. run_id={run_id} dataset_id={dataset_id}")
if __name__ == "__main__":
    main()



