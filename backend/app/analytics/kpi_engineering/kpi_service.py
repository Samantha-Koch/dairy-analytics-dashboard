from backend.app.analytics.kpi_engineering.kpi_registry import KPI_REGISTRY

def compute_kpi(kpi_name: str, customer_id: str | None):
    if kpi_name not in KPI_REGISTRY:
        raise ValueError(f"KPI '{kpi_name}' not found")

    entry = KPI_REGISTRY[kpi_name]
    func = entry["function"]
    unit = entry["unit"]
    has_usda = entry["has_usda_data"]

   
  
    result = func(customer_id=customer_id)

    customer_avg = result.get("customer_avg")
    customer_trend = result.get("customer_trend", [])
    dates = result.get("dates", [])

    customer_data_exists = (
        customer_avg is not None or
        (isinstance(customer_trend, list) and len(customer_trend) > 0)
    )

    response = {
        "kpi_name": kpi_name,
        "unit": unit,
        "has_usda_data": has_usda,
        "customer_data_exists": customer_data_exists,
        "customer_avg": customer_avg,
        "customer_trend": customer_trend,
        "dates": dates,
    }

    if has_usda:
        response["usda_avg"] = result.get("usda_avg")

    return response
