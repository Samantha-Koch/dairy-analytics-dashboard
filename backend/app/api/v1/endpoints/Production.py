from fastapi import APIRouter, Query
from typing import Literal, Optional
from backend.app.analytics.sql import fetch_dataframe
import numpy as np

router = APIRouter()

SourceType = Literal["usda", "customer", "both"]
FrequencyType = Literal["annual", "monthly"]

#USDA metric_id (unique)
MILK_YIELD_METRIC_ID_MONTHLY = "dairy_situation__milk_production__milk_per_cow"
MILK_YIELD_METRIC_IDS_ANNUAL = [
    "cop_2005__supporting_information__output_per_cow_(pounds)",
    "cop_2010__supporting_information__output_per_cow_(pounds)",
    "cop_2016__supporting_information__output_per_cow",
    "cop_2021__supporting_information__output_per_cow",
]

SCC_METRIC_ID = "som_cell__lmprs__component"
BUTTERFAT_METRIC_ID = "milk_butterfat__lmprs__component"
PROTEIN_METRIC_ID = "milk_protein__lmprs__component"


#USDA milk yield aids

def get_usda_milk_yield_monthly(year: str):
    query = f"""
        SELECT
            time_id AS time,
            value AS usda_value
        FROM fact_observation
        WHERE metric_id = '{MILK_YIELD_METRIC_ID_MONTHLY}'
          AND time_id LIKE '{year}-%%'
        ORDER BY time_id;
    """
    return fetch_dataframe(query)


def get_usda_milk_yield_annual():
    query = """
        SELECT
            time_id AS year,
            value / 12 AS usda_value
        FROM fact_observation
        WHERE metric_id IN (
            'cop_2005__supporting_information__output_per_cow_(pounds)',
            'cop_2010__supporting_information__output_per_cow_(pounds)',
            'cop_2016__supporting_information__output_per_cow',
            'cop_2021__supporting_information__output_per_cow'
        )
        ORDER BY year;
    """
    return fetch_dataframe(query)


#USDA SCC aids

def get_usda_scc_monthly(year: str):
    query = f"""
        SELECT
            time_id AS time,
            value * 1000 AS usda_value
        FROM fact_observation
        WHERE metric_id = '{SCC_METRIC_ID}'
          AND time_id LIKE '{year}%%'
        ORDER BY time_id;
    """
    return fetch_dataframe(query)


def get_usda_scc_annual():
    query = f"""
        SELECT
            LEFT(source_period, 4) AS year,
            AVG(value) * 1000 AS usda_value
        FROM fact_observation
        WHERE metric_id = '{SCC_METRIC_ID}'
        GROUP BY LEFT(source_period, 4)
        ORDER BY year;
    """
    return fetch_dataframe(query)


#USDA butterfat aids

def get_usda_butterfat_monthly(year: str):
    query = f"""
        SELECT
            time_id AS time,
            value AS usda_value
        FROM fact_observation
        WHERE metric_id = '{BUTTERFAT_METRIC_ID}'
          AND time_id LIKE '{year}%%'
        ORDER BY time_id;
    """
    return fetch_dataframe(query)


def get_usda_butterfat_annual():
    query = f"""
        SELECT
            LEFT(source_period, 4) AS year,
            AVG(value) AS usda_value
        FROM fact_observation
        WHERE metric_id = '{BUTTERFAT_METRIC_ID}'
        GROUP BY LEFT(source_period, 4)
        ORDER BY year;
    """
    return fetch_dataframe(query)


#USDA protein aids

def get_usda_protein_monthly(year: str):
    query = f"""
        SELECT
            time_id AS time,
            value AS usda_value
        FROM fact_observation
        WHERE metric_id = '{PROTEIN_METRIC_ID}'
          AND time_id LIKE '{year}%%'
        ORDER BY time_id;
    """
    return fetch_dataframe(query)


def get_usda_protein_annual():
    query = f"""
        SELECT
            LEFT(source_period, 4) AS year,
            AVG(value) AS usda_value
        FROM fact_observation
        WHERE metric_id = '{PROTEIN_METRIC_ID}'
        GROUP BY LEFT(source_period, 4)
        ORDER BY year;
    """
    return fetch_dataframe(query)


#customer aids

def get_customer_monthly(year: str, customer_id: str, metric_name: str):
    query = f"""
        SELECT time_id AS time, AVG(value) AS customer_value
        FROM farm_data_long
        WHERE customer_id = '{customer_id}'
        AND metric = '{metric_name}'
        AND year = '{year}'
        GROUP BY time_id
        ORDER BY time_id;

    """
    return fetch_dataframe(query)


def get_customer_annual(customer_id: str, metric_name: str):
    query = f"""
        SELECT year, AVG(value) AS customer_value
        FROM farm_data_long
        WHERE customer_id = '{customer_id}'
        AND metric = '{metric_name}'
        GROUP BY year
        ORDER BY year;

    """
    return fetch_dataframe(query)


#merger

def merge_usda_customer(usda_df, customer_df, frequency: FrequencyType):
    time_col = "year" if frequency == "annual" else "time"

    if usda_df is None and customer_df is None:
        return []

    if usda_df is None:
        merged = customer_df.copy()
        merged["usda_value"] = None
        merged.rename(columns={time_col: "time"}, inplace=True)
        merged = merged.replace({np.nan: None})
        return merged.to_dict(orient="records")

    if customer_df is None:
        merged = usda_df.copy()
        merged["customer_value"] = None
        merged.rename(columns={time_col: "time"}, inplace=True)
        merged = merged.replace({np.nan: None})
        return merged.to_dict(orient="records")

    merged = usda_df.merge(customer_df, on=time_col, how="outer")
    merged.sort_values(by=time_col, inplace=True)
    merged.rename(columns={time_col: "time"}, inplace=True)

    merged = merged.replace({np.nan: None})
    return merged.to_dict(orient="records")


#year availability aids

def get_available_years_usda_metric(metric_id: str):
    query = f"""
        SELECT DISTINCT LEFT(source_period, 4) AS year
        FROM fact_observation
        WHERE metric_id = '{metric_id}'
        ORDER BY year;
    """
    df = fetch_dataframe(query)
    return [int(y) for y in df["year"].tolist()]


def get_available_years_usda_items(items: list[str]):
    items_str = "', '".join(items)
    query = f"""
        SELECT DISTINCT LEFT(source_period, 4) AS year
        FROM fact_observation
        WHERE metric_id IN ('{items_str}')
        ORDER BY year;
    """
    df = fetch_dataframe(query)
    return [int(y) for y in df["year"].tolist()]

def get_available_years_usda_milk_yield_monthly():
    query = f"""
        SELECT DISTINCT LEFT(time_id, 4) AS year
        FROM fact_observation
        WHERE metric_id = '{MILK_YIELD_METRIC_ID_MONTHLY}'
            AND source_period != 'Annual'
        ORDER BY year;
    """
    df = fetch_dataframe(query)
    return [int(y) for y in df["year"].tolist()]


def get_available_years_customer(metric_name: str):
    query = f"""
        SELECT DISTINCT year
        FROM farm_data_long
        WHERE metric = '{metric_name}'
        ORDER BY year;
    """
    df = fetch_dataframe(query)
    return [int(y) for y in df["year"].tolist()]


def combine_years(usda_years, customer_years):
    return sorted(set(usda_years or []) | set(customer_years or []))


#milk yield endpoint

@router.get("/milk_yield")
def get_milk_yield(
    source: SourceType = Query("both"),
    frequency: FrequencyType = Query("annual"),
    year: Optional[str] = Query(None),
    customer_id: Optional[str] = Query(None),
):
    usda_df = None
    customer_df = None

    if source in ("usda", "both"):
        if frequency == "monthly":
            if not year:
                return {"mode": "monthly", "data": []}
            usda_df = get_usda_milk_yield_monthly(year)
        else:
            usda_df = get_usda_milk_yield_annual()

    if source in ("customer", "both") and customer_id:
        if frequency == "monthly":
            if not year:
                return {"mode": "monthly", "data": []}
            customer_df = get_customer_monthly(year, customer_id, "milk yield")
        else:
            customer_df = get_customer_annual(customer_id, "milk yield")

    data = merge_usda_customer(usda_df, customer_df, frequency)
    return {"mode": frequency, "year": year if frequency == "monthly" else None, "data": data}


@router.get("/milk_yield/available_years")
def get_milk_yield_available_years():
    usda_years_monthly = get_available_years_usda_milk_yield_monthly()
    customer_years = get_available_years_customer("milk yield")
    return {"years": combine_years(usda_years_monthly, customer_years)}


#scc endpoint

@router.get("/scc")
def get_scc(
    source: SourceType = Query("both"),
    frequency: FrequencyType = Query("annual"),
    year: Optional[str] = Query(None),
    customer_id: Optional[str] = Query(None),
):
    usda_df = None
    customer_df = None

    if source in ("usda", "both"):
        if frequency == "monthly":
            if not year:
                return {"mode": "monthly", "data": []}
            usda_df = get_usda_scc_monthly(year)
        else:
            usda_df = get_usda_scc_annual()

    if source in ("customer", "both") and customer_id:
        if frequency == "monthly":
            if not year:
                return {"mode": "monthly", "data": []}
            customer_df = get_customer_monthly(year, customer_id, "bulk tank SCC")
        else:
            customer_df = get_customer_annual(customer_id, "bulk tank SCC")

    data = merge_usda_customer(usda_df, customer_df, frequency)
    return {"mode": frequency, "year": year if frequency == "monthly" else None, "data": data}


@router.get("/scc/available_years")
def get_scc_available_years():
    usda_years = get_available_years_usda_metric(SCC_METRIC_ID)
    customer_years = get_available_years_customer("bulk tank SCC")
    return {"years": combine_years(usda_years, customer_years)}


#butterfat endpoint

@router.get("/butterfat")
def get_butterfat(
    source: SourceType = Query("both"),
    frequency: FrequencyType = Query("annual"),
    year: Optional[str] = Query(None),
    customer_id: Optional[str] = Query(None),
):
    usda_df = None
    customer_df = None

    if source in ("usda", "both"):
        if frequency == "monthly":
            if not year:
                return {"mode": "monthly", "data": []}
            usda_df = get_usda_butterfat_monthly(year)
        else:
            usda_df = get_usda_butterfat_annual()

    if source in ("customer", "both") and customer_id:
        if frequency == "monthly":
            if not year:
                return {"mode": "monthly", "data": []}
            customer_df = get_customer_monthly(year, customer_id, "butterfat percent")
        else:
            customer_df = get_customer_annual(customer_id, "butterfat percent")

    data = merge_usda_customer(usda_df, customer_df, frequency)
    return {"mode": frequency, "year": year if frequency == "monthly" else None, "data": data}


@router.get("/butterfat/available_years")
def get_butterfat_available_years():
    usda_years = get_available_years_usda_metric(BUTTERFAT_METRIC_ID)
    customer_years = get_available_years_customer("butterfat percent")
    return {"years": combine_years(usda_years, customer_years)}


#protein endpoint

@router.get("/protein")
def get_protein(
    source: SourceType = Query("both"),
    frequency: FrequencyType = Query("annual"),
    year: Optional[str] = Query(None),
    customer_id: Optional[str] = Query(None),
):
    usda_df = None
    customer_df = None

    if source in ("usda", "both"):
        if frequency == "monthly":
            if not year:
                return {"mode": "monthly", "data": []}
            usda_df = get_usda_protein_monthly(year)
        else:
            usda_df = get_usda_protein_annual()

    if source in ("customer", "both") and customer_id:
        if frequency == "monthly":
            if not year:
                return {"mode": "monthly", "data": []}
            customer_df = get_customer_monthly(year, customer_id, "protein percent")
        else:
            customer_df = get_customer_annual(customer_id, "protein percent")

    data = merge_usda_customer(usda_df, customer_df, frequency)
    return {"mode": frequency, "year": year if frequency == "monthly" else None, "data": data}


@router.get("/protein/available_years")
def get_protein_available_years():
    usda_years = get_available_years_usda_metric(PROTEIN_METRIC_ID)
    customer_years = get_available_years_customer("protein percent")
    return {"years": combine_years(usda_years, customer_years)}
