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
    # Fetch customer time series
    dates_rev, gross_rev = get_customer_timeseries(customer_id, "gross revenue")
    dates_costs, total_costs = get_customer_timeseries(customer_id, "total costs")
    dates_milk, milk_yield = get_customer_timeseries(customer_id, "milk yield")

    # Build dictionaries keyed by date
    rev_map = dict(zip(dates_rev, gross_rev))
    costs_map = dict(zip(dates_costs, total_costs))
    milk_map = dict(zip(dates_milk, milk_yield))

    common_dates = sorted(set(dates_rev) & set(dates_costs) & set(dates_milk))

    full_trend = []
    for d in common_dates:
        g = rev_map.get(d)
        c = costs_map.get(d)
        m = milk_map.get(d)

        if g is not None and c is not None and m is not None:
            full_trend.append((g - c) * (m / 100))
        else:
            full_trend.append(None)

    customer_trend = full_trend[-12:]
    dates = common_dates[-12:]

    # Latest customer value
    customer_avg = (
        customer_trend[-1]
        if customer_trend and customer_trend[-1] is not None
        else None
    )

    # USDA values
    gvp = get_usda_latest_by_source_item("Total, gross value of production")
    costs = get_usda_latest_by_source_item("Total, costs listed")
    milk_per_cow = get_usda_latest_by_source_item("Milk per cow")

    if gvp is not None and costs is not None and milk_per_cow is not None:
        usda_margin = (gvp - costs) * (milk_per_cow / 100)
    else:
        usda_margin = None

    return {
        "customer_avg": customer_avg,
        "customer_trend": customer_trend,
        "dates": dates,
        "usda_avg": usda_margin,
    }
