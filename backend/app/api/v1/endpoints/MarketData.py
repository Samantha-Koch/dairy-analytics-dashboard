from fastapi import APIRouter, Query
from backend.app.analytics.sql import fetch_dataframe

router = APIRouter()

@router.get("/milk_class_prices")
async def get_milk_class_prices(year: str = Query("all")):
    """
    Returns milk class prices with unified CPI-style time_id format.
    """

    # Monthly data
    if year != "all":
        query = f"""
            SELECT
                source_period AS time, 
                MAX(CASE WHEN source_data_item = 'ClassIWhole' THEN value END) AS class_i,
                MAX(CASE WHEN source_data_item = 'ClassIIWhole' THEN value END) AS class_ii,
                MAX(CASE WHEN source_data_item = 'ClassIIIWhole' THEN value END) AS class_iii,
                MAX(CASE WHEN source_data_item = 'ClassIVWhole' THEN value END) AS class_iv
            FROM fact_observation
            WHERE source_data_item IN (
                'ClassIWhole',
                'ClassIIWhole',
                'ClassIIIWhole',
                'ClassIVWhole'
            )
            AND source_period LIKE '{year}%%'
            GROUP BY source_period, time_id
            ORDER BY time_id;
        """
        df = fetch_dataframe(query)
        return {
            "mode": "monthly",
            "year": year,
            "data": df.to_dict(orient="records")
        }
    else : 
        query = """
            SELECT
                LEFT(source_period, 4) AS year,
                AVG(CASE WHEN source_data_item = 'ClassIWhole' THEN value END) AS class_i,
                AVG(CASE WHEN source_data_item = 'ClassIIWhole' THEN value END) AS class_ii,
                AVG(CASE WHEN source_data_item = 'ClassIIIWhole' THEN value END) AS class_iii,
                AVG(CASE WHEN source_data_item = 'ClassIVWhole' THEN value END) AS class_iv
            FROM fact_observation
            WHERE source_data_item IN (
                'ClassIWhole',
                'ClassIIWhole',
                'ClassIIIWhole',
                'ClassIVWhole'
            )
            GROUP BY LEFT(source_period, 4)
            ORDER BY year;
        """
        df = fetch_dataframe(query)
        return {
            "mode": "yearly",
            "data": df.to_dict(orient="records")
        }


@router.get("/milk_comp_prices")
async def get_milk_comp_prices(year: str = Query("all")):
    """
    Returns butterfat and protein prices with unified CPI-style time_id format.
    """

    # Monthly data
    if year != "all":
        query = f"""
            SELECT
                source_period AS time,
                MAX(CASE WHEN source_data_item = 'butterfat' THEN value END) AS butterfat,
                MAX(CASE WHEN source_data_item = 'protein' THEN value END) AS protein
            FROM fact_observation
            WHERE source_data_item IN ('butterfat', 'protein')
            AND source_period LIKE '{year}%%'
            GROUP BY source_period, time_id
            ORDER BY time_id;
        """
        df = fetch_dataframe(query)
        return {
            "mode": "monthly",
            "year": year,
            "data": df.to_dict(orient="records")
        }

    # Yearly averages
    query = """
        SELECT
            LEFT(source_period, 4) AS year,
            AVG(CASE WHEN source_data_item = 'butterfat' THEN value END) AS butterfat,
            AVG(CASE WHEN source_data_item = 'protein' THEN value END) AS protein
        FROM fact_observation
        WHERE source_data_item IN ('butterfat', 'protein')
        GROUP BY LEFT(source_period, 4)
        ORDER BY year;
    """
    df = fetch_dataframe(query)
    return {
        "mode": "yearly",
        "data": df.to_dict(orient="records")
    }

@router.get("/butter_prices")
async def get_butter_prices(year: str = Query("all")):
    """
    Returns butter price data from Wholesale dairy product prices.
    """

    # Monthly or yearly depending on time_id format
    if year != "all":
        query = f"""
            SELECT
                time_id,
                value AS butter_price
            FROM fact_observation
            WHERE source_category = 'Wholesale dairy product prices'
            AND source_data_item = 'Butter'
            AND source_period LIKE '{year}-%%'
            ORDER BY time_id;
        """
        df = fetch_dataframe(query)
        return {
            "mode": "monthly",
            "year": year,
            "data": df.to_dict(orient="records")
        }

    # Yearly averages
    query = """
        SELECT
            time_id AS year,
            value AS butter_price
        FROM fact_observation
        WHERE source_category = 'Wholesale dairy product prices'
        AND source_data_item = 'Butter'
        AND source_period = 'Annual'
        ORDER BY year;
    """
    df = fetch_dataframe(query)
    return {
        "mode": "yearly",
        "data": df.to_dict(orient="records")
    }

@router.get("/cheese_prices")
async def get_cheese_prices(year: str = Query("all")):
    """
    Returns cheese price data from Wholesale dairy product prices.
    """

    if year != "all":
        query = f"""
            SELECT
                time_id,
                value AS cheese_price
            FROM fact_observation
            WHERE source_category = 'Wholesale dairy product prices'
            AND source_data_item = 'Cheddar cheese, 40-pound blocks'
            AND source_period LIKE '{year}-%%'
            ORDER BY time_id;
        """
        df = fetch_dataframe(query)
        return {
            "mode": "monthly",
            "year": year,
            "data": df.to_dict(orient="records")
        }

    query = """
        SELECT
            time_id AS year,
            value AS cheese_price
        FROM fact_observation
        WHERE source_category = 'Wholesale dairy product prices'
        AND source_data_item = 'Cheddar cheese, 40-pound blocks'
        AND source_period = 'Annual'
        ORDER BY year;
    """
    df = fetch_dataframe(query)
    return {
        "mode": "yearly",
        "data": df.to_dict(orient="records")
    }
