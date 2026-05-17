from backend.app.analytics.kpi_sql import (
    get_customer_timeseries,
    get_usda_latest_by_source_item,
)


def milk_class(customer_id: str):
    # USDA-only KPI
    usda_values = {
        "ClassIWhole": get_usda_latest_by_source_item("ClassIWhole"),
        "ClassIIWhole": get_usda_latest_by_source_item("ClassIIWhole"),
        "ClassIIIWhole": get_usda_latest_by_source_item("ClassIIIWhole"),
        "ClassIVWhole": get_usda_latest_by_source_item("ClassIVWhole"),
    }

    return {
        "customer_avg": None,
        "customer_trend": [],
        "dates": [],
        "usda_avg": usda_values,
    }


def margin_per_cow(customer_id: str):
    # Customer data
    dates_rev, gross_rev = get_customer_timeseries(customer_id, "gross revenue")
    dates_costs, total_costs = get_customer_timeseries(customer_id, "total costs")
    dates_milk, milk_yield = get_customer_timeseries(customer_id, "milk yield")  # per-cow output

    # Align dates (use dates from milk yield)
    dates = dates_milk

    # Compute customer margin per cow
    if gross_rev and total_costs and milk_yield:
        customer_avg = (gross_rev[-1] - total_costs[-1]) * (milk_yield[-1] / 100)
    else:
        customer_avg = None

    # USDA data
    gvp = get_usda_latest_by_source_item("Total, gross value of production")
    costs = get_usda_latest_by_source_item("Total, costs listed")
    milk_per_cow = get_usda_latest_by_source_item("Milk per cow")

    # Compute USDA margin per cow
    if gvp is not None and costs is not None and milk_per_cow is not None:
        usda_margin = (gvp - costs) * (milk_per_cow / 100)
    else:
        usda_margin = None

    return {
        "customer_avg": customer_avg,
        "customer_trend": [],  # margin trend not computed yet
        "dates": dates,
        "usda_avg": {
            "Total, gross value of production": gvp,
            "Total, costs listed": costs,
            "Milk per cow": milk_per_cow,
            "usda_margin_per_cow": usda_margin,
        },
    }
