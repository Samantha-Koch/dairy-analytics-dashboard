from analysis.utils.sql import (
    get_customer_timeseries,
    get_usda_average,
)
def feed_efficiency(customer_id: str):
    dates, cust_values = get_customer_timeseries(customer_id, "feed_efficiency")
    usda_avg = get_usda_average("feed_efficiency")
    customer_avg = cust_values[-1] if cust_values else None
    return {
        "customer_avg": customer_avg,
        "customer_trend": cust_values,
        "dates": dates,
        "usda_avg": usda_avg,
    }
def income_over_feed(customer_id: str):
    dates, cust_values = get_customer_timeseries(customer_id, "income_over_feed")
    usda_avg = get_usda_average("income_over_feed")
    customer_avg = cust_values[-1] if cust_values else None
    return {
        "customer_avg": customer_avg,
        "customer_trend": cust_values,
        "dates": dates,
        "usda_avg": usda_avg,
    }