
from fastapi import APIRouter
from backend.app.analytics.kpi_engineering.kpi_service import compute_kpi
from backend.app.analytics.kpi_engineering.kpi_registry import KPI_REGISTRY

router = APIRouter()

@router.get("/summary")
def get_dashboard_summary(customer_id: str | None = None):
    summary = {}

    for kpi_name, meta in KPI_REGISTRY.items():
        try:
            summary[kpi_name] = compute_kpi(kpi_name, customer_id)
        except Exception:
            summary[kpi_name] = {
                "error": f"Failed to compute KPI '{kpi_name}'"
            }

    return {
        "status": "ok",
        "message": "Dashboard summary generated",
        "data": summary,
    }
