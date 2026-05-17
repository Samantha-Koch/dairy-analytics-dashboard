from backend.app.analytics.kpi_sql import get_customer_timeseries

def mastitis_prev(customer_id: str):
    dates, values = get_customer_timeseries(customer_id, "mastitis prevalence")

    return {
        "customer_avg": values[-1] if values else None,
        "customer_trend": values,
        "dates": dates,
        "usda_avg": None,
    }


def dry_period(customer_id: str):
    dates, values = get_customer_timeseries(customer_id, "dry period")

    return {
        "customer_avg": values[-1] if values else None,
        "customer_trend": values,
        "dates": dates,
        "usda_avg": None,
    }
