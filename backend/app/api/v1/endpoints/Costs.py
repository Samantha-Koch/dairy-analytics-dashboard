from fastapi import APIRouter

router = APIRouter()

@router.get("/summary")
def get_costs_summary():
    return {
        "status": "ok",
        "message": "Costs summary endpoint is working",
        "data": {
            "example_metric": 123,
            "another_metric": 456
        }
    }
