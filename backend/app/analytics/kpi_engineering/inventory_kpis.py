from backend.app.analytics.kpi_sql import get_customer_timeseries

def spoilage_rate(customer_id: str):
    dates, values = get_customer_timeseries(customer_id, "spoilage rate")

    return {
        "customer_avg": values[-1] if values else None,
        "customer_trend": values,
        "dates": dates,
        "usda_avg": None,
    }
