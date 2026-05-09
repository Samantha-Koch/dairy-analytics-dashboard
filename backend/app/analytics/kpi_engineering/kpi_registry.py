# analysis/kpi_engineering/kpi_registry.py

from .production_kpis import milk_yield, butterfat_percent, protein_percent, bulk_scc
from .feed_kpis import feed_efficiency, income_over_feed
from .health_kpis import mastitis_prev, dry_period
from .inventory_kpis import spoilage_rate
from .market_kpis import milk_class, margin_per_cow

KPI_REGISTRY = {
    
    "milk_yield": {
        "function": milk_yield,
        "unit": "pounds",
        "has_usda_data": False,
        "customer_data_exists": True,
    },
    "butterfat_percentage": {
        "function": butterfat_percent,
        "unit": "percent",
        "has_usda_data": True,
        "customer_data_exists": True,
    },
    "protein_percentage": {
        "function": protein_percent,
        "unit": "percent",
        "has_usda_data": True,
        "customer_data_exists": True,
    },
    "bulk_scc": {
        "function": bulk_scc,
        "unit": "cells per mL",
        "has_udsa_data": True,
        "customer_data_exists": True,
    },
    "feed_efficiency": {
        "function": feed_efficiency,
        "unit": "ECM/DMI",
        "has_usda_data": True,
        "customer_data_exists": True,
    },
    "income_over_feed": {
        "function": income_over_feed,
        "unit": "$/cow/day",
        "has_usda_data": True,
        "customer_data_exists": True,
    },
    "milk_class": {
        "function": milk_class,
        "unit": "dollars_per_cwt",
        "has_usda_data": True,
        "customer_data_exists": False,
    },
    "margin_per_cow": {
        "function": margin_per_cow,
        "unit": "dollars_per_cow",
        "has_usda_data": True,
        "customer_data_exists": True,
    },

    # KPIs WITHOUT USDA DATA
    "subclinical_mastitis_prevalence": {
        "function": mastitis_prev,
        "unit": "percent",
        "has_usda_data": False,
        "customer_data_exists": True,
    },
    "dry_period": {
        "function": dry_period,
        "unit": "days",
        "has_usda_data": False,
        "customer_data_exists": True,
    },
    "spoilage_rate": {
        "function": spoilage_rate,
        "unit": "pounds per month",
        "has_usda_data": False,
        "customer_data_exists": True,
    },
}
