# analysis/kpi_engineering/production_kpis.py

from backend.app.analytics.kpi_sql import (
    get_customer_timeseries,
    get_usda_latest_by_metric_id
)

def milk_yield(customer_id: str):
    dates, values = get_customer_timeseries(customer_id, "total milk yield")

    return {
        "customer_avg": values[-1] if values else None,
        "customer_trend": values,
        "dates": dates,
        "usda_avg": None,
    }


def butterfat_percent(customer_id: str):
    dates, values = get_customer_timeseries(customer_id, "butterfat percent")
    usda_avg = get_usda_latest_by_metric_id("milk_butterfat__lmprs__component")

    return {
        "customer_avg": values[-1] if values else None,
        "customer_trend": values,
        "dates": dates,
        "usda_avg": usda_avg,
    }


def protein_percent(customer_id: str):
    dates, values = get_customer_timeseries(customer_id, "protein percent")
    usda_avg = get_usda_latest_by_metric_id("milk_protein__lmprs__component")
    return {
        "customer_avg": values[-1] if values else None,
        "customer_trend": values,
        "dates": dates,
        "usda_avg": usda_avg,
    }


def bulk_scc(customer_id: str):
    dates, values = get_customer_timeseries(customer_id, "bulk tank SCC")
    usda_avg = get_usda_latest_by_metric_id("som_cell__lmprs__component")
    return {
        "customer_avg": values[-1] if values else None,
        "customer_trend": values,
        "dates": dates,
        "usda_avg": usda_avg,
    }
