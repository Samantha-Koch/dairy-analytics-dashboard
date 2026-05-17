# analysis/kpi_engineering/production_kpis.py

from backend.app.analytics.kpi_sql import (
    get_customer_timeseries,
    get_usda_latest_by_metric_id
)

def milk_yield(customer_id: str):
    dates, cust_values = get_customer_timeseries(customer_id, "total milk yield")
    customer_avg = cust_values[-1] if cust_values else None
    return {
        "customer_avg": customer_avg,
        "customer_trend": cust_values,
        "dates": dates,
        # No USDA data for milk yield
    }


def butterfat_percent(customer_id: str):
    dates, cust_values = get_customer_timeseries(customer_id, "butterfat percent")
    usda_avg = get_usda_latest_by_metric_id("milk_butterfat__lmprs__component")
    customer_avg = cust_values[-1] if cust_values else None
    return {
        "customer_avg": customer_avg,
        "customer_trend": cust_values,
        "dates": dates,
        "usda_avg": usda_avg,
    }


def protein_percent(customer_id: str):
    dates, cust_values = get_customer_timeseries(customer_id, "protein percent")
    usda_avg = get_usda_latest_by_metric_id("milk_protein__lmprs__component")
    customer_avg = cust_values[-1] if cust_values else None
    return {
        "customer_avg": customer_avg,
        "customer_trend": cust_values,
        "dates": dates,
        "usda_avg": usda_avg,
    }


def bulk_scc(customer_id: str):
    dates, cust_values = get_customer_timeseries(customer_id, "bulk tank SCC")
    usda_avg = get_usda_latest_by_metric_id("som_cell__lmprs__component")
    customer_avg = cust_values[-1] if cust_values else None
    return {
        "customer_avg": customer_avg,
        "customer_trend": cust_values,
        "dates": dates,
        "usda_avg": usda_avg,
    }
