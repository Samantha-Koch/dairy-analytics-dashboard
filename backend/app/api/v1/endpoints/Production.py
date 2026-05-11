from fastapi import APIRouter

router = APIRouter()

@router.get("/summary")
def get_production_summary():
    return {
        "status": "ok",
        "message": "Production summary endpoint is working",
        "data": {
            "example_metric": 123,
            "another_metric": 456
        }
    }
@router.get("/milk_yield")
async def get_milk_yield(year: str = Query("all")):
    """
    Returns average milk yield with unified CPI-style time_id format.
    """

    # Monthly data
    if source != "USDA":
        query = f"""
            SELECT
                value / 12 AS month_avg, time_id AS year
            FROM fact_observation
            WHERE source_data_item = 'Milk per cow'
            AND source_period = 'ANNUAL'
            GROUP BY source_period
            ORDER BY source_period;
        """
        df = fetch_dataframe(query)
        return {
            "mode": "USDA",
            "year": year,
            "data": df.to_dict(orient="records")
        }
    else : 
        return("add customer data")