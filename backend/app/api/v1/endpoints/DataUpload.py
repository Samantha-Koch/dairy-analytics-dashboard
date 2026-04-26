from fastapi import APIRouter

router = APIRouter()

@router.get("/summary")
def get_data_upload_summary():
    return {
        "status": "ok",
        "message": "Data upload summary endpoint is working",
        "data": {
            "example_metric": 123,
            "another_metric": 456
        }
    }
