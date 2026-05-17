from kpi_registry import KPI_REGISTRY
from backend.app.analytics.kpi_sql import (
    get_customer_timeseries,
    get_customer_timeseries_monthly,
    get_usda_average,
)

def compute_kpi(kpi_name: str, customer_id: str):
    if kpi_name not in KPI_REGISTRY:
        raise ValueError(f"KPI '{kpi_name}' not found")

    entry = KPI_REGISTRY[kpi_name]
    func = entry["function"]
    unit = entry["unit"]
    has_usda = entry["has_usda_data"]
    has_customer = entry.get("customer_data_exists", True)
    needs_monthly_agg = entry.get("needs_monthly_aggregation", False)

    # ---------------------------------------------------------
    # USDA-only KPI (like milk_class)
    # ---------------------------------------------------------
    if not has_customer:
        result = func(customer_id=customer_id)

        return {
            "kpi_name": kpi_name,
            "unit": unit,
            "has_usda_data": has_usda,
            "customer_data_exists": False,
            "customer_avg": None,
            "customer_trend": [],
            "dates": [],
            "usda_avg": result.get("usda_avg"),
        }

    # ---------------------------------------------------------
    # Customer KPIs (with or without USDA)
    # ---------------------------------------------------------
    if needs_monthly_agg:
        dates, cust_values = get_customer_timeseries_monthly(customer_id, kpi_name)
    else:
        dates, cust_values = get_customer_timeseries(customer_id, kpi_name)

    customer_avg = cust_values[-1] if cust_values else None

    response = {
        "kpi_name": kpi_name,
        "unit": unit,
        "has_usda_data": has_usda,
        "customer_data_exists": True,
        "customer_avg": customer_avg,
        "customer_trend": cust_values,
        "dates": dates,
    }

    if has_usda:
        response["usda_avg"] = get_usda_average(kpi_name)

    return response
