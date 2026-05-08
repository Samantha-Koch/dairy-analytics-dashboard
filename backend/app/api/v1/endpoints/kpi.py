from fastapi import APIRouter, HTTPException
from analysis.kpi_engineering.kpi_service import compute_kpi

router = APIRouter()

@router.get("/kpi/{kpi_name}")
def get_kpi(kpi_name: str, customer_id: str):
    try:
        return compute_kpi(kpi_name, customer_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
