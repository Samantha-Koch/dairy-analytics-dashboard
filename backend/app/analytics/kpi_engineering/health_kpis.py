from backend.app.analytics.kpi_sql import (
    get_customer_timeseries,
)
def mastitis_prev(customer_id: str):
    dates, cust_values = get_customer_timeseries(customer_id, "mastitis prevalence")
    customer_avg = cust_values[-1] if cust_values else None
    return {
        "customer_avg": customer_avg,
        "customer_trend": cust_values,
        "dates": dates,
    }
def dry_period(customer_id: str):
    dates, cust_values = get_customer_timeseries(customer_id, "dry period")
    customer_avg = cust_values[-1] if cust_values else None
    return {
        "customer_avg": customer_avg,
        "customer_trend": cust_values,
        "dates": dates,
    }