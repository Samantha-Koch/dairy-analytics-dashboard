# backend/app/analytics/kpi_sql.py

import pandas as pd
from app.analytics.sql import fetch_dataframe



# CUSTOMER DATA AIDS

def get_customer_timeseries(customer_id: str, metric: str):
    """
    Returns (dates, values) for a given customer + metric.
    Dates are sorted ascending.
    """
    query = f"""
        SELECT date, value
        FROM public.farm_data_long
        WHERE customer_id = '{customer_id}'
          AND metric = '{metric}'
        ORDER BY date;
    """

    df = fetch_dataframe(query)

    if df.empty:
        return [], []

    # Ensure correct types
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")

    dates = df["date"].dt.strftime("%Y-%m-%d").tolist()
    values = df["value"].astype(float).tolist()

    return dates, values


def get_customer_timeseries_monthly(customer_id: str, metric: str):
    """
    Monthly-aggregated version of get_customer_timeseries.
    Uses date_trunc('month').
    """
    query = f"""
        SELECT date_trunc('month', date) AS month, AVG(value) AS value
        FROM public.farm_data_long
        WHERE customer_id = '{customer_id}'
          AND metric = '{metric}'
        GROUP BY month
        ORDER BY month;
    """

    df = fetch_dataframe(query)

    if df.empty:
        return [], []

    df["month"] = pd.to_datetime(df["month"])
    df = df.sort_values("month")

    dates = df["month"].dt.strftime("%Y-%m-%d").tolist()
    values = df["value"].astype(float).tolist()

    return dates, values


#USDA AIDS

def get_usda_average_by_metric_id(metric_id: str):
    """
    Returns a single numeric USDA average for a given metric_id.
    """
    query = f"""
        SELECT AVG(value) AS avg_value
        FROM public.fact_observation
        WHERE metric_id = '{metric_id}';
    """

    df = fetch_dataframe(query)

    if df.empty or df["avg_value"].iloc[0] is None:
        return None

    return float(df["avg_value"].iloc[0])


def get_usda_average_by_source_item(source_item: str):
    """
    Returns a single numeric USDA average for a given source_data_item.
    """
    query = f"""
        SELECT AVG(value) AS avg_value
        FROM public.fact_observation
        WHERE source_data_item = '{source_item}';
    """

    df = fetch_dataframe(query)

    if df.empty or df["avg_value"].iloc[0] is None:
        return None

    return float(df["avg_value"].iloc[0])


def get_usda_latest_by_source_item(source_item: str):
    """
    Returns the most recent USDA value for a given source_data_item.
    Useful for KPIs like milk_class or feed efficiency.
    """
    query = f"""
        SELECT time_id, value
        FROM public.fact_observation
        WHERE source_data_item = '{source_item}'
        ORDER BY time_id DESC
        LIMIT 1;
    """

    df = fetch_dataframe(query)

    if df.empty:
        return None

    return float(df["value"].iloc[0])


def get_usda_latest_by_metric_id(metric_id: str):
    """
    Returns the most recent USDA value for a given metric_id.
    """
    query = f"""
        SELECT time_id, value
        FROM public.fact_observation
        WHERE metric_id = '{metric_id}'
        ORDER BY time_id DESC
        LIMIT 1;
    """

    df = fetch_dataframe(query)

    if df.empty:
        return None

    return float(df["value"].iloc[0])



# USDA MULTI-ITEM AIDS (for milk_class, feed_efficiency, margin_per_cow)

def get_usda_latest_multiple_source_items(items: list[str]):
    """
    Returns a dict: { source_data_item: latest_value }
    """
    results = {}
    for item in items:
        results[item] = get_usda_latest_by_source_item(item)
    return results


def get_usda_latest_multiple_metric_ids(metric_ids: list[str]):
    """
    Returns a dict: { metric_id: latest_value }
    """
    results = {}
    for mid in metric_ids:
        results[mid] = get_usda_latest_by_metric_id(mid)
    return results
