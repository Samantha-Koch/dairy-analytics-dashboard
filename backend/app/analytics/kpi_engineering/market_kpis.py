from analysis.utils.sql import (
    get_customer_timeseries,
    get_usda_average,
)
def milk_class(customer_id: str):
    dates, cust_values = get_customer_timeseries(customer_id, "milk_class")
    usda_avg = get_usda_average("milk_class")
    customer_avg = cust_values[-1] if cust_values else None
    return {
        "customer_avg": None,
        "customer_trend": [],
        "dates": [],
        "usda_avg": usda_avg,
    }
def margin_per_cow(customer_id: str):
    dates, cust_values = get_customer_timeseries(customer_id, "margin_per_cow")
    usda_avg = get_usda_average("margin_per_cow")
    customer_avg = cust_values[-1] if cust_values else None
    return {
        "customer_avg": customer_avg,
        "customer_trend": cust_values,
        "dates": dates,
        "usda_avg": usda_avg,
    }