from backend.app.analytics.kpi_sql import (
    get_customer_timeseries,
    get_usda_latest_by_source_item,
)

def feed_efficiency(customer_id: str):
    # CUSTOMER DATA
    dates_milk, total_milk = get_customer_timeseries(customer_id, "total milk yield")
    dates_feed, total_feed = get_customer_timeseries(customer_id, "total feed")
    dates_bf, bf_percent = get_customer_timeseries(customer_id, "butterfat percent")
    dates_pr, pr_percent = get_customer_timeseries(customer_id, "protein percent")

    # Align dates (use milk dates)
    dates = dates_milk

    # Compute customer feed efficiency
    if total_milk and total_feed and bf_percent and pr_percent:
        TM = total_milk[-1]
        TF = total_feed[-1]
        BF = bf_percent[-1]
        PR = pr_percent[-1]

        customer_avg = (
            ((0.327 * TM)
            + (12.95 * (BF/100) * TM)
            + (7.2 * (PR/100) * TM))
        ) / TF
    else:
        customer_avg = None

    # Trend (optional: using total_milk as placeholder)
    customer_trend = total_milk if total_milk else []

    return {
        "customer_avg": customer_avg,
        "customer_trend": customer_trend,
        "dates": dates,
        "usda_avg": None,
    }


def income_over_feed(customer_id: str):
    # CUSTOMER DATA
    dates_milk, milk_yield = get_customer_timeseries(customer_id, "milk yield")
    dates_feed, feed_costs = get_customer_timeseries(customer_id, "total feed costs")
    dates_rev, gross_rev = get_customer_timeseries(customer_id, "gross revenue")

    # Compute customer IOFC
    if milk_yield and feed_costs and gross_rev:
        MY = milk_yield[-1]
        FC = feed_costs[-1]
        GR = gross_rev[-1]

        customer_avg = (GR * 0.8) * (MY / 100) - (FC * (MY / 100))
    else:
        customer_avg = None

    # USDA DATA
    price = get_usda_latest_by_source_item("Average price paid for milk")
    feed_costs_usda = get_usda_latest_by_source_item("Total, feed costs")
    MP = get_usda_latest_by_source_item("Milk per cow")

    if price and feed_costs_usda and MP:
        usda_avg = (price * (MP / 100)) - (feed_costs_usda * (MP / 100))
    else:
        usda_avg = None

    return {
        "customer_avg": customer_avg,
        "customer_trend": milk_yield if milk_yield else [],
        "dates": dates_milk,
        "usda_avg": usda_avg,
    }

