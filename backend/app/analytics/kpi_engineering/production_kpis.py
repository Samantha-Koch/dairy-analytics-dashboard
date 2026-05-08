# analysis/kpi_engineering/production_kpis.py

from analysis.utils.sql import (
    get_customer_timeseries,
    get_usda_average,
)

def milk_yield(customer_id: str):
    dates, cust_values = get_customer_timeseries(customer_id, "milk_yield")
    customer_avg = cust_values[-1] if cust_values else None
    return {
        "customer_avg": customer_avg,
        "customer_trend": cust_values,
        "dates": dates,
        # No USDA data for milk yield
    }


def butterfat_percent(customer_id: str):
    dates, cust_values = get_customer_timeseries(customer_id, "butterfat_percentage")
    usda_avg = get_usda_average("butterfat_percentage")
    customer_avg = cust_values[-1] if cust_values else None
    return {
        "customer_avg": customer_avg,
        "customer_trend": cust_values,
        "dates": dates,
        "usda_avg": usda_avg,
    }


def protein_percent(customer_id: str):
    dates, cust_values = get_customer_timeseries(customer_id, "protein_percentage")
    usda_avg = get_usda_average("protein_percentage")
    customer_avg = cust_values[-1] if cust_values else None
    return {
        "customer_avg": customer_avg,
        "customer_trend": cust_values,
        "dates": dates,
        "usda_avg": usda_avg,
    }


def bulk_scc(customer_id: str):
    dates, cust_values = get_customer_timeseries(customer_id, "bulk_scc")
    usda_avg = get_usda_average("bulk_scc")
    customer_avg = cust_values[-1] if cust_values else None
    return {
        "customer_avg": customer_avg,
        "customer_trend": cust_values,
        "dates": dates,
        "usda_avg": usda_avg,
    }
