from analysis.utils.sql import (
    get_customer_timeseries,
    get_usda_average,
)
def spoilage_rate(customer_id: str):
    dates, cust_values = get_customer_timeseries(customer_id, "spoilage_rate")
    customer_avg = cust_values[-1] if cust_values else None
    return {
        "customer_avg": customer_avg,
        "customer_trend": cust_values,
        "dates": dates,
    }