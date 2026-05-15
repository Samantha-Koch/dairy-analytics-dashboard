from fastapi import APIRouter, Query
from typing import Literal, Optional, List
from backend.app.analytics.sql import fetch_dataframe
import numpy as np

router = APIRouter()

SourceType = Literal["usda", "customer", "both"]
FrequencyType = Literal["annual", "monthly"]

#USDA config

USDA_DATASET_IDS: List[str] = [
    "f942076b-d682-5c45-97a5-c83957553fd7",
    "8e7bf481-00a7-5fb7-a806-6adf6bebd052",
    "923947b0-87c4-57d4-abac-9c7f01860796",
    "bee61711-5a27-5918-a6d9-f11da57ebb09",
    "fa826992-7625-51cc-a0cc-fb1e58412c3f",
]

USDA_TOTAL_COSTS_ITEM = "Total, costs listed"
USDA_TOTAL_FEED_COSTS_ITEM = "Total, feed costs"
USDA_MILK_FEED_RATIO_ITEM = "Milk-feed ratio"
USDA_GROSS_VALUE_ITEM = "Total, gross value of production"
USDA_MILK_PER_COW_ITEM = "Output per cow"


#merger
def merge_usda_customer(usda_df, customer_df, frequency: FrequencyType):
    time_col = "year" if frequency == "annual" else "time"

    if usda_df is None and customer_df is None:
        return []

    if usda_df is None:
        merged = customer_df.copy()
        merged["usda_value"] = None
        merged.rename(columns={time_col: "time"}, inplace=True)
        return merged.replace({np.nan: None}).to_dict(orient="records")

    if customer_df is None:
        merged = usda_df.copy()
        merged["customer_value"] = None
        merged.rename(columns={time_col: "time"}, inplace=True)
        return merged.replace({np.nan: None}).to_dict(orient="records")

    merged = usda_df.merge(customer_df, on=time_col, how="outer")
    merged.sort_values(by=time_col, inplace=True)
    merged.rename(columns={time_col: "time"}, inplace=True)
    return merged.replace({np.nan: None}).to_dict(orient="records")


#customer years

def get_available_years_customer_metric(metric_names: List[str]):
    metrics_str = "', '".join(metric_names)
    query = f"""
        SELECT DISTINCT year
        FROM farm_data_long
        WHERE metric IN ('{metrics_str}')
        ORDER BY year;
    """
    df = fetch_dataframe(query)
    return [int(y) for y in df["year"].tolist()]


#USDA aids

def get_usda_simple_annual(source_item: str):
    datasets_str = "', '".join(USDA_DATASET_IDS)
    query = f"""
        SELECT time_id AS year, value AS usda_value
        FROM fact_observation
        WHERE dataset_id IN ('{datasets_str}')
          AND source_data_item = '{source_item}'
          AND time_id::int >= 2000
        ORDER BY year;
    """
    return fetch_dataframe(query)


def get_usda_net_revenue_annual():
    datasets_str = "', '".join(USDA_DATASET_IDS)
    query = f"""
        SELECT
            time_id AS year,
            MAX(CASE WHEN source_data_item = '{USDA_GROSS_VALUE_ITEM}' THEN value END)
            -
            MAX(CASE WHEN source_data_item = '{USDA_TOTAL_COSTS_ITEM}' THEN value END)
            AS usda_value
        FROM fact_observation
        WHERE dataset_id IN ('{datasets_str}')
          AND source_data_item IN ('{USDA_GROSS_VALUE_ITEM}', '{USDA_TOTAL_COSTS_ITEM}')
        GROUP BY time_id
        ORDER BY year;
    """
    return fetch_dataframe(query)


def get_usda_margin_per_cow_annual():
    datasets_str = "', '".join(USDA_DATASET_IDS)
    query = f"""
        SELECT
            time_id AS year,
            (
                MAX(CASE WHEN source_data_item = '{USDA_GROSS_VALUE_ITEM}' THEN value END)
                -
                MAX(CASE WHEN source_data_item = '{USDA_TOTAL_COSTS_ITEM}' THEN value END)
            )
            *
            (
                MAX(CASE WHEN source_data_item = '{USDA_MILK_PER_COW_ITEM}' THEN value END) / 100.0
            )
            AS usda_value
        FROM fact_observation
        WHERE dataset_id IN ('{datasets_str}')
          AND source_data_item IN (
              '{USDA_GROSS_VALUE_ITEM}',
              '{USDA_TOTAL_COSTS_ITEM}',
              '{USDA_MILK_PER_COW_ITEM}'
          )
        GROUP BY time_id
        ORDER BY year;
    """
    return fetch_dataframe(query)


def get_usda_milk_feed_ratio_annual():
    return get_usda_simple_annual(USDA_MILK_FEED_RATIO_ITEM)


#customer aids

def get_customer_simple_monthly(year: str, customer_id: str, metric_name: str):
    query = f"""
        SELECT time_id AS time, value AS customer_value
        FROM farm_data_long
        WHERE customer_id = '{customer_id}'
          AND metric = '{metric_name}'
          AND year = '{year}'
        ORDER BY time_id;
    """
    return fetch_dataframe(query)


def get_customer_simple_annual(customer_id: str, metric_name: str):
    query = f"""
        SELECT year, AVG(value) AS customer_value
        FROM farm_data_long
        WHERE customer_id = '{customer_id}'
          AND metric = '{metric_name}'
        GROUP BY year
        ORDER BY year;
    """
    return fetch_dataframe(query)



def get_customer_milk_feed_ratio_monthly(year: str, customer_id: str):
    query = f"""
        SELECT
            time_id AS time,
            (MAX(CASE WHEN metric = 'total milk yield' THEN value END))
            /
            NULLIF(MAX(CASE WHEN metric = 'total feed' THEN value END), 0)
            AS customer_value
        FROM farm_data_long
        WHERE customer_id = '{customer_id}'
          AND metric IN ('total milk yield', 'total feed')
          AND year = '{year}'
        GROUP BY time_id
        ORDER BY time_id;
    """
    return fetch_dataframe(query)


def get_customer_milk_feed_ratio_annual(customer_id: str):
    query = f"""
        SELECT
            year,
            AVG(CASE WHEN metric = 'total milk yield' THEN value END)
            /
            NULLIF(AVG(CASE WHEN metric = 'total feed' THEN value END), 0)
            AS customer_value
        FROM farm_data_long
        WHERE customer_id = '{customer_id}'
          AND metric IN ('total milk yield', 'total feed')
        GROUP BY year
        ORDER BY year;
    """
    return fetch_dataframe(query)


def get_customer_net_revenue_monthly(year: str, customer_id: str):
    query = f"""
        SELECT
            time_id AS time,
            MAX(CASE WHEN metric = 'gross revenue' THEN value END)
            -
            MAX(CASE WHEN metric = 'total costs' THEN value END)
            AS customer_value
        FROM farm_data_long
        WHERE customer_id = '{customer_id}'
          AND metric IN ('gross revenue', 'total costs')
          AND year = '{year}'
        GROUP BY time_id
        ORDER BY time_id;
    """
    return fetch_dataframe(query)


def get_customer_net_revenue_annual(customer_id: str):
    query = f"""
        SELECT
            year,
            AVG(CASE WHEN metric = 'gross revenue' THEN value END)
            -
            AVG(CASE WHEN metric = 'total costs' THEN value END)
            AS customer_value
        FROM farm_data_long
        WHERE customer_id = '{customer_id}'
          AND metric IN ('gross revenue', 'total costs')
        GROUP BY year
        ORDER BY year;
    """
    return fetch_dataframe(query)


def get_customer_margin_per_cow_monthly(year: str, customer_id: str):
    query = f"""
        SELECT
            time_id AS time,
            (
                MAX(CASE WHEN metric = 'gross revenue' THEN value END)
                -
                MAX(CASE WHEN metric = 'total costs' THEN value END)
            )
            *
            (
                MAX(CASE WHEN metric = 'milk yield' THEN value END) / 100.0
            )
            AS customer_value
        FROM farm_data_long
        WHERE customer_id = '{customer_id}'
          AND metric IN ('gross revenue', 'total costs', 'milk yield')
          AND year = '{year}'
        GROUP BY time_id
        ORDER BY time_id;
    """
    return fetch_dataframe(query)


def get_customer_margin_per_cow_annual(customer_id: str):
    query = f"""
        SELECT
            year,
            (
                AVG(CASE WHEN metric = 'gross revenue' THEN value END)
                -
                AVG(CASE WHEN metric = 'total costs' THEN value END)
            )
            *
            (
                AVG(CASE WHEN metric = 'milk yield' THEN value END) / 100.0
            )
            AS customer_value
        FROM farm_data_long
        WHERE customer_id = '{customer_id}'
          AND metric IN ('gross revenue', 'total costs', 'milk yield')
        GROUP BY year
        ORDER BY year;
    """
    return fetch_dataframe(query)


#endpoints

@router.get("/total_costs")
def get_total_costs(
    source: SourceType = Query("both"),
    frequency: FrequencyType = Query("annual"),
    year: Optional[str] = Query(None),
    customer_id: Optional[str] = Query(None),
):
    usda_df = get_usda_simple_annual(USDA_TOTAL_COSTS_ITEM) if source in ("usda", "both") else None

    customer_df = None
    if source in ("customer", "both") and customer_id:
        customer_df = (
            get_customer_simple_monthly(year, customer_id, "total costs")
            if frequency == "monthly" and year
            else get_customer_simple_annual(customer_id, "total costs")
        )

    return {
        "mode": frequency,
        "year": year if frequency == "monthly" else None,
        "data": merge_usda_customer(usda_df, customer_df, frequency),
    }


@router.get("/total_costs/available_years")
def get_total_costs_available_years():
    return {"years": get_available_years_customer_metric(["total costs"])}



@router.get("/total_feed_costs")
def get_total_feed_costs(
    source: SourceType = Query("both"),
    frequency: FrequencyType = Query("annual"),
    year: Optional[str] = Query(None),
    customer_id: Optional[str] = Query(None),
):
    usda_df = get_usda_simple_annual(USDA_TOTAL_FEED_COSTS_ITEM) if source in ("usda", "both") else None

    customer_df = None
    if source in ("customer", "both") and customer_id:
        customer_df = (
            get_customer_simple_monthly(year, customer_id, "total feed costs")
            if frequency == "monthly" and year
            else get_customer_simple_annual(customer_id, "total feed costs")
        )

    return {
        "mode": frequency,
        "year": year if frequency == "monthly" else None,
        "data": merge_usda_customer(usda_df, customer_df, frequency),
    }


@router.get("/total_feed_costs/available_years")
def get_total_feed_costs_available_years():
    return {"years": get_available_years_customer_metric(["total feed costs"])}



@router.get("/milk_feed_ratio")
def get_milk_feed_ratio(
    source: SourceType = Query("both"),
    frequency: FrequencyType = Query("annual"),
    year: Optional[str] = Query(None),
    customer_id: Optional[str] = Query(None),
):
    usda_df = get_usda_milk_feed_ratio_annual() if source in ("usda", "both") else None

    customer_df = None
    if source in ("customer", "both") and customer_id:
        customer_df = (
            get_customer_milk_feed_ratio_monthly(year, customer_id)
            if frequency == "monthly" and year
            else get_customer_milk_feed_ratio_annual(customer_id)
        )

    return {
        "mode": frequency,
        "year": year if frequency == "monthly" else None,
        "data": merge_usda_customer(usda_df, customer_df, frequency),
    }


@router.get("/milk_feed_ratio/available_years")
def get_milk_feed_ratio_available_years():
    return {"years": get_available_years_customer_metric(["total milk yield", "total feed"])}



@router.get("/net_revenue")
def get_net_revenue(
    source: SourceType = Query("both"),
    frequency: FrequencyType = Query("annual"),
    year: Optional[str] = Query(None),
    customer_id: Optional[str] = Query(None),
):
    usda_df = get_usda_net_revenue_annual() if source in ("usda", "both") else None

    customer_df = None
    if source in ("customer", "both") and customer_id:
        customer_df = (
            get_customer_net_revenue_monthly(year, customer_id)
            if frequency == "monthly" and year
            else get_customer_net_revenue_annual(customer_id)
        )

    return {
        "mode": frequency,
        "year": year if frequency == "monthly" else None,
        "data": merge_usda_customer(usda_df, customer_df, frequency),
    }


@router.get("/net_revenue/available_years")
def get_net_revenue_available_years():
    return {"years": get_available_years_customer_metric(["gross revenue", "total costs"])}



@router.get("/margin_per_cow")
def get_margin_per_cow(
    source: SourceType = Query("both"),
    frequency: FrequencyType = Query("annual"),
    year: Optional[str] = Query(None),
    customer_id: Optional[str] = Query(None),
):
    usda_df = get_usda_margin_per_cow_annual() if source in ("usda", "both") else None

    customer_df = None
    if source in ("customer", "both") and customer_id:
        customer_df = (
            get_customer_margin_per_cow_monthly(year, customer_id)
            if frequency == "monthly" and year
            else get_customer_margin_per_cow_annual(customer_id)
        )

    return {
        "mode": frequency,
        "year": year if frequency == "monthly" else None,
        "data": merge_usda_customer(usda_df, customer_df, frequency),
    }


@router.get("/margin_per_cow/available_years")
def get_margin_per_cow_available_years():
    return {"years": get_available_years_customer_metric(["gross revenue", "total costs", "milk yield"])}

