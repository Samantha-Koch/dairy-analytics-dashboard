# analysis/kpi_engineering/kpi_registry.py

from .production_kpis import milk_yield, butterfat_percent, protein_percent, bulk_scc
from .feed_kpis import feed_efficiency, income_over_feed
from .health_kpis import mastitis_prev, dry_period
from .inventory_kpis import spoilage_rate
from .market_kpis import milk_class, margin_per_cow

KPI_REGISTRY = {

    # -------------------------
    # PRODUCTION KPIs
    # -------------------------
    "milk_yield": {
        "function": milk_yield,
        "unit": "CWT",
        "has_usda_data": False,
        "customer_metric": "milk yield",
    },
    "butterfat_percentage": {
        "function": butterfat_percent,
        "unit": "%",
        "has_usda_data": True,
        "customer_metric": "butterfat percent",
    },
    "protein_percentage": {
        "function": protein_percent,
        "unit": "%",
        "has_usda_data": True,
        "customer_metric": "protein percent",
    },
    "bulk_scc": {
        "function": bulk_scc,
        "unit": "cells/mL",
        "has_usda_data": True,
        "customer_metric": "bulk tank SCC",
    },

    # -------------------------
    # FEED & REVENUE KPIs
    # (multi‑metric → no customer_metric)
    # -------------------------
    "feed_efficiency": {
        "function": feed_efficiency,
        "unit": "ECM/DMI",
        "has_usda_data": False,
    },
    "income_over_feed": {
        "function": income_over_feed,
        "unit": "$/cow/day",
        "has_usda_data": True,
    },

    # -------------------------
    # MARKET KPIs
    # -------------------------
    "milk_class": {
        "function": milk_class,
        "unit": "$/CWT",
        "has_usda_data": True,
        # USDA‑only KPI → no customer_metric
    },
    "margin_per_cow": {
        "function": margin_per_cow,
        "unit": "$/CWT",
        "has_usda_data": True,
        # multi‑metric → no customer_metric
    },

    # -------------------------
    # HEALTH KPIs
    # -------------------------
    "subclinical_mastitis_prevalence": {
        "function": mastitis_prev,
        "unit": "%",
        "has_usda_data": False,
        "customer_metric": "mastitis prevalence",
    },
    "dry_period": {
        "function": dry_period,
        "unit": "days",
        "has_usda_data": False,
        "customer_metric": "dry period",
    },

    # -------------------------
    # INVENTORY KPIs
    # -------------------------
    "spoilage_rate": {
        "function": spoilage_rate,
        "unit": "%",
        "has_usda_data": False,
        "customer_metric": "spoilage rate",
    },
}
