from fastapi import APIRouter

router = APIRouter()

@router.get("/summary")
def get_market_data_summary():
    return {
        "status": "ok",
        "message": "Market data summary endpoint is working",
        "data": {
            "example_metric": 123,
            "another_metric": 456
        }
    }
