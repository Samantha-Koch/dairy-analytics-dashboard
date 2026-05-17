from backend.app.analytics.kpi_sql import (
    get_customer_timeseries,
    get_usda_latest_by_source_item,
    get_usda_latest_by_metric_id,
)

def feed_efficiency(customer_id: str):
    # CUSTOMER DATA ONLY
    _, total_milk = get_customer_timeseries(customer_id, "total milk yield")
    _, total_feed = get_customer_timeseries(customer_id, "total feed")
    _, bf_percent = get_customer_timeseries(customer_id, "butterfat percent")
    _, pr_percent = get_customer_timeseries(customer_id, "protein percent")

    if total_milk and total_feed and bf_percent and pr_percent:
        TM = total_milk[-1]
        TF = total_feed[-1]
        BF = bf_percent[-1]
        PR = pr_percent[-1]

        customer_avg = (
            (0.327 * TM)
            + (12.95 * BF * TM)
            + (7.2 * PR * TM)
        ) / TF
    else:
        customer_avg = None

    return {
        "customer_avg": customer_avg,
        "customer_trend": total_milk,  # or compute a trend later
        "dates": [],  # optional: use total_milk dates
        "usda_avg": None,  # USDA not applicable
    }



def income_over_feed(customer_id: str):
    # -------------------------
    # CUSTOMER DATA
    # -------------------------
    _, milk_yield = get_customer_timeseries(customer_id, "milk yield")
    _, feed_costs = get_customer_timeseries(customer_id, "total feed costs")
    _, gross_rev = get_customer_timeseries(customer_id, "gross revenue")

    if milk_yield and feed_costs and gross_rev:
        MY = milk_yield[-1]
        FC = feed_costs[-1]
        GR = gross_rev[-1]

        customer_avg = (GR * 0.8) * (MY / 100) - (FC * (MY / 100))
    else:
        customer_avg = None

    # -------------------------
    # USDA DATA
    # -------------------------
    price = get_usda_latest_by_source_item("Average price paid for milk   ($/cwt)")
    feed_costs_usda = get_usda_latest_by_source_item("Total, feed costs    ($/cwt)")
    MP = get_usda_latest_by_source_item("Milk per cow")

    if price and feed_costs_usda and MP:
        usda_avg = (price * (MP / 100)) - (feed_costs_usda * MP)
    else:
        usda_avg = None

    return {
        "customer_avg": customer_avg,
        "customer_trend": milk_yield,
        "dates": [],
        "usda_avg": usda_avg,
    }
