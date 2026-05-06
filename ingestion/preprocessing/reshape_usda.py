import pandas as pd
import os
import argparse

import ast

def load_lmprs_results_csv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)

    # Normalize columns
    df.columns = [c.strip().lower() for c in df.columns]

    if "results" not in df.columns:
        raise ValueError("LMPRS file does not contain a 'results' column.")

    # Extract the JSON list from the single row
    raw_list_str = df["results"].iloc[0]

    # Convert Python-style list of dicts into real Python objects
    records = ast.literal_eval(raw_list_str)

    # Convert to DataFrame
    return pd.DataFrame(records)



def load_file(path: str) -> pd.DataFrame:
    ext = os.path.splitext(path)[1].lower()
    if ext in [".xls", ".xlsx"]:
        return pd.read_excel(path)
    elif ext == ".csv":
        return pd.read_csv(path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")

def assign_default_category_if_empty(df, default="milk_factors"):
    
    if "category" not in df.columns:
        df["category"] = default
        return df  # nothing to do

    # Normalize category column
    cat = df["category"].astype(str).str.strip().str.lower()

    # Check if all values are empty or NaN
    empty_mask = cat.isna() | (cat == "") | (cat == "nan") | (cat == "none")
    if empty_mask.all():
        df["category"] = default
    return df

def is_long_format(df: pd.DataFrame) -> bool: 
    cols = set(df.columns.str.lower())
    return (
        "value" in cols and 
        ("item" in cols or "data_item" in cols) and
        "year" in cols
    )
def normalize_period(row):
    # Quarterly formats like JAN-MAR
    q = str(row["period"]).upper().replace(" ", "").replace("-", "_")
    quarter_map = {
        "JAN_MAR": "jan_mar",
        "APR_JUN": "apr_jun",
        "JUL_SEP": "jul_sep",
        "OCT_DEC": "oct_dec",
    }
    if q in quarter_map:
        return quarter_map[q]

    # Monthly formats like January, February
    month_map = {
        "JANUARY": "JAN",
        "FEBRUARY": "FEB",
        "MARCH": "MAR",
        "APRIL": "APR",
        "MAY": "MAY",
        "JUNE": "JUN",
        "JULY": "JUL",
        "AUGUST": "AUG",
        "SEPTEMBER": "SEP",
        "OCTOBER": "OCT",
        "NOVEMBER": "NOV",
        "DECEMBER": "DEC",
    }
    m = str(row["period"]).strip().upper()
    if m in month_map:
        return f"{int(row['year'])}-{month_map[m]}"

    return row["period"]


def reshape_long_format(df: pd.DataFrame) -> pd.DataFrame:
    # Normalize column names
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

    # Ensure period exists
    if "period" not in df.columns:
        df["period"] = "annual"

    # Ensure category exists
    if "category" not in df.columns:
        df["category"] = None

    # Ensure unit exists
    if "unit" not in df.columns and "units" in df.columns:
        df["unit"] = df["units"]

    # Normalize period if year + period exist
    if "year" in df.columns and "period" in df.columns:
        df["period"] = df.apply(normalize_period, axis=1)

    return df


def reshape_wide_to_long(df: pd.DataFrame) -> pd.DataFrame:
    # Normalize column names
    df.columns = [c.strip().replace(" ", "_").replace("-", "_") for c in df.columns]

    # Ensure year exists
    if "report_year" in df.columns:
        df["year"] = df["report_year"].astype(int)

    # Build USDA‑compatible period codes BEFORE melting (Class Prices only)
    if "report_month" in df.columns and "report_year" in df.columns:
        df["period"] = df.apply(
            lambda r: f"{int(r['report_year'])}-{str(r['report_month'])[:3].upper()}",
            axis=1
        )
    else:
        df["period"] = None

    # Identify class price columns
    class_price_cols = [c for c in df.columns if c.lower().startswith("class")]

    # Identify component columns (Butterfat, Protein, etc.)
    component_cols = [
        c for c in df.columns
        if c.lower() in [
            "butterfat", "protein", "nfs", "othersolids",
            "somaticcellcount", "receipts"
        ]
    ]

    # Identify month columns (Producer Components)
    month_map = {
        "jan": "JAN", "feb": "FEB", "mar": "MAR", "apr": "APR",
        "may": "MAY", "jun": "JUN", "jul": "JUL", "aug": "AUG",
        "sep": "SEP", "oct": "OCT", "nov": "NOV", "dec": "DEC",
    }
    month_cols = [c for c in df.columns if c.lower() in month_map]

    # CASE 1: Class Prices or explicit component columns
    if class_price_cols or component_cols:
        value_cols = class_price_cols + component_cols
        id_cols = [c for c in df.columns if c not in value_cols]

        df_long = df.melt(
            id_vars=id_cols,
            value_vars=value_cols,
            var_name="data_item",
            value_name="value"
        )

        # Period already built above for Class Prices
        if df_long["period"].isna().all():
            df_long["period"] = "annual"

    # CASE 2: Producer Components (SomCell, Butterfat, NFS, etc.)
    elif month_cols:
        id_cols = [c for c in df.columns if c not in month_cols]

        df_long = df.melt(
            id_vars=id_cols,
            value_vars=month_cols,
            var_name="month",
            value_name="value"
        )

        # Build period from year + melted month
        df_long["month"] = df_long["month"].str.lower().map(month_map)
        df_long["period"] = df_long.apply(
            lambda r: f"{int(r['year'])}-{r['month']}" if pd.notnull(r["year"]) else None,
            axis=1
        )

        # Label the component (SomCell, Butterfat, etc.)
        # Use reportSection if available
        if "reportsection" in df.columns:
            component_name = df["reportsection"].iloc[0].lower()
        else:
            component_name = "component"

        df_long["data_item"] = component_name
        df_long = df_long.drop(columns=["month"], errors="ignore")

    # CASE 3: Nothing to melt
    else:
        df_long = df.copy()
        df_long["data_item"] = None
        df_long["value"] = None

    # Add category + unit
    df_long["category"] = "lmprs"
    df_long["unit"] = None

    return df_long


def reshape_usda(input_path: str, output_path: str):
    df = load_file(input_path)
    df.columns = [c.strip().lower() for c in df.columns]

    # LMPRS detection: detect by column name, not by row value
    if "results" in df.columns:
        df = load_lmprs_results_csv(input_path)


    # Now detect long vs wide
    if is_long_format(df):
        df_out = reshape_long_format(df)
    else:
        df_out = reshape_wide_to_long(df)

    df = assign_default_category_if_empty(df, default="milk_factors")

    df_out.to_csv(output_path, index=False)
    print(f"Saved long-format CSV → {output_path}")



def main():
    parser = argparse.ArgumentParser(description="USDA preprocessing: auto-detect long vs wide format.")
    parser.add_argument("--input", required=True, help="Path to raw USDA file")
    parser.add_argument("--output", required=True, help="Path to save long-format CSV")
    args = parser.parse_args()

    reshape_usda(args.input, args.output)


if __name__ == "__main__":
    main() 