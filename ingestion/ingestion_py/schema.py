from __future__ import annotations

from sqlalchemy import text
from sqlalchemy.engine import Engine


def ensure_schema(engine: Engine) -> None:
   
    ddl = [
        # dim_time
        """
        CREATE TABLE IF NOT EXISTS dim_time (
            time_id TEXT PRIMARY KEY,
            period_type TEXT NOT NULL CHECK (period_type IN ('year','quarter','month')),
            year INTEGER NOT NULL,
            quarter INTEGER NULL CHECK (quarter BETWEEN 1 AND 4),
            month INTEGER NULL CHECK (month BETWEEN 1 AND 12),
            period_start DATE NOT NULL,
            period_end DATE NOT NULL,
            UNIQUE (period_type, year, quarter, month)
        );
        """,
        # dim_geo (minimal)
        """
        CREATE TABLE IF NOT EXISTS dim_geo (
            geo_id TEXT PRIMARY KEY,
            geo_level TEXT NOT NULL CHECK (geo_level IN ('national','state','fmmo_order')),
            scheme TEXT NOT NULL,
            code TEXT NULL,
            name TEXT NOT NULL,
            parent_geo_id TEXT NULL REFERENCES dim_geo(geo_id),
            fips TEXT NULL,
            state_abbr TEXT NULL,
            UNIQUE (scheme, code)
        );
        """,
        # dim_entity (minimal)
        """
        CREATE TABLE IF NOT EXISTS dim_entity (
            entity_id TEXT PRIMARY KEY,
            entity_type TEXT NOT NULL CHECK (entity_type IN ('usda','user')),
            display_name TEXT NOT NULL,
            owner_user_id TEXT NULL,
            default_geo_id TEXT NULL REFERENCES dim_geo(geo_id),
            metadata_json JSONB NULL
        );
        """,
        # dataset / dataset_run
        """
        CREATE TABLE IF NOT EXISTS dataset (
            dataset_id TEXT PRIMARY KEY,
            dataset_slug TEXT NOT NULL UNIQUE,
            dataset_type TEXT NOT NULL CHECK (dataset_type IN ('usda','user_upload')),
            name TEXT NOT NULL,
            provider TEXT NULL,
            refresh_cadence TEXT NULL,
            raw_uri TEXT NULL,
            notes TEXT NULL
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS dataset_run (
            run_id UUID PRIMARY KEY,
            dataset_id TEXT NOT NULL REFERENCES dataset(dataset_id),
            status TEXT NOT NULL CHECK (status IN ('started','succeeded','failed')),
            started_at TIMESTAMPTZ NOT NULL,
            finished_at TIMESTAMPTZ NULL,
            stats_json JSONB NULL,
            error_json JSONB NULL,
            code_version TEXT NULL
        );
        """,
        # dim_metric
        """
        CREATE TABLE IF NOT EXISTS dim_metric (
            metric_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            allowed_period_types TEXT[] NOT NULL,
            description TEXT NULL,
            domain TEXT NULL,
            base_unit TEXT NULL,
            value_type TEXT NULL,
            aggregation TEXT NULL
        );
        """,
        # metric_source_map
        """
        CREATE TABLE IF NOT EXISTS metric_source_map (
            dataset_id TEXT NOT NULL REFERENCES dataset(dataset_id),
            source_category TEXT NULL,
            source_data_item TEXT NOT NULL,
            metric_id TEXT NOT NULL REFERENCES dim_metric(metric_id),
            PRIMARY KEY (dataset_id, source_category, source_data_item)
        );
        """,
        # fact_observation
        """
        CREATE TABLE IF NOT EXISTS fact_observation (
            observation_id UUID PRIMARY KEY,
            metric_id TEXT NOT NULL REFERENCES dim_metric(metric_id),
            time_id TEXT NOT NULL REFERENCES dim_time(time_id),
            geo_id TEXT NOT NULL REFERENCES dim_geo(geo_id),
            entity_id TEXT NOT NULL REFERENCES dim_entity(entity_id),
            value NUMERIC NOT NULL,
            unit TEXT NULL,
            source TEXT NOT NULL CHECK (source IN ('usda','user_upload','derived')),
            dataset_id TEXT NULL REFERENCES dataset(dataset_id),
            run_id UUID NULL REFERENCES dataset_run(run_id),
            source_series_id TEXT NULL,
            source_category TEXT NULL,
            source_data_item TEXT NULL,
            source_period TEXT NULL,
            quality_flag TEXT NULL,
            ingested_at TIMESTAMPTZ NOT NULL,
            UNIQUE (metric_id, time_id, geo_id, entity_id)
        );
        """,
    ]

    with engine.begin() as conn:
        for stmt in ddl:
            conn.execute(text(stmt))

