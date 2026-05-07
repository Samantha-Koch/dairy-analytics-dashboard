import os
import re
import pandas as pd


KNOWN_STATES = [
    "california", "florida", "georgia", "idaho", "illinois",
    "indiana", "iowa", "kentucky", "maine", "michigan",
    "minnesota", "missouri", "new mexico", "new york",
    "ohio", "oregon", "pennsylvania", "tennessee", "texas",
    "vermont", "virginia", "washington", "wisconsin", "all states"
]


def find_header_row(df_raw: pd.DataFrame) -> int:
    """
    Find the row index that contains the state names (header row).
    We look in the first ~15 rows for any known state name.
    """
    for i in range(min(15, len(df_raw))):
        row = df_raw.iloc[i].astype(str).str.lower()
        if any(state in row.values for state in KNOWN_STATES):
            return i
    raise ValueError("Could not find header row with state names.")


def assign_category_from_item(item: str, current_category: str) -> (str, str):
    """
    Given a data_item string and the current category, return:
      (category_for_this_row, updated_current_category)

    Section headers update the current_category but do NOT themselves
    get a category (they'll be dropped later when values are NaN).
    """
    text = str(item).strip().lower()

    # Section headers
    if text.startswith("gross value of production"):
        return None, "gross_value_of_production"
    if text.startswith("operating costs"):
        return None, "operating_costs"
    if text.startswith("allocated overhead"):
        return None, "allocated_overhead"
    if text.startswith("total costs listed"):
        # standalone category row with values
        return "total_costs", "total_costs"
    if text.startswith("value of production less"):
        # both "less total costs listed" and "less operating costs"
        return "net_value", "net_value"
    if text.startswith("supporting information"):
        return None, "supporting_information"

    # Regular row: inherit current category
    return current_category, current_category


def infer_unit(data_item: str) -> str:
    """
    Infer unit from the data_item text.
    Defaults to dollars_per_cwt for cost/value rows.
    """
    text = (data_item or "").lower()

    if "head per farm" in text:
        return "head_per_farm"
    if "pounds" in text:
        return "pounds"
    if "percent of farms" in text:
        return "percent_of_farms"
    if "percent of sales" in text:
        return "percent_of_sales"
    if "percent" in text:
        return "percent"

    # Default for cost/value rows
    return "dollars_per_cwt"


def parse_old_cop_excel(path: str) -> pd.DataFrame:
    """
    Parse legacy COP Excel files (2005, 2010) formatted as report-style sheets.

    Output columns:
        year
        period
        state
        category
        data_item
        value
        unit
    """
    xls = pd.ExcelFile(path)
    all_years = []

    for sheet in xls.sheet_names:
        # Only process sheets that look like years (e.g., "2005", "2010")
        sheet_name = str(sheet).strip()
        if not re.fullmatch(r"\d{4}", sheet_name):
            continue

        year = int(sheet_name)
        df_raw = xls.parse(sheet, header=None)

        # 1. Find header row with state names
        header_row_idx = find_header_row(df_raw)
        header = df_raw.iloc[header_row_idx].fillna("")

        header = header.astype(str).str.strip()
        df = df_raw.iloc[header_row_idx + 1:].copy()
        df.columns = header.values

        # Drop completely empty rows
        df = df.dropna(how="all")
        if df.empty:
            continue

        # 2. data_item = first column
        metric_col = df.columns[0]
        df["data_item"] = df[metric_col].astype(str).str.strip()

        # 3. Assign categories based on section headers + running state
        categories = []
        current_category = None
        for item in df["data_item"]:
            cat_for_row, current_category = assign_category_from_item(item, current_category)
            categories.append(cat_for_row)

        df["category"] = categories

        # 4. Identify state columns (everything except metric + helper cols)
        state_cols = [
            c for c in df.columns
            if c not in [metric_col, "data_item", "category"]
        ]

        # 5. Melt to long format
        df_long = df.melt(
            id_vars=["data_item", "category"],
            value_vars=state_cols,
            var_name="state",
            value_name="value"
        )

        # 6. Clean value column
        df_long["value"] = (
            df_long["value"]
            .astype(str)
            .str.replace(",", "", regex=False)
            .str.strip()
        )
        df_long["value"] = pd.to_numeric(df_long["value"], errors="coerce")

        # 7. Drop rows with no data_item and no value
        df_long = df_long.dropna(subset=["data_item"], how="all")
        df_long = df_long.dropna(subset=["value"], how="all")

        # 8. Drop pure section-header rows (no category and no numeric value)
        # (Most will already be dropped by value NaN, but this is extra safety.)
        df_long = df_long[df_long["data_item"].str.strip() != ""]

        # 9. Infer units per data_item
        df_long["unit"] = df_long["data_item"].apply(infer_unit)

        # 10. Add year/period and normalize state names
        df_long["year"] = year
        df_long["period"] = "annual"
        df_long["state"] = df_long["state"].astype(str).str.strip()

        # Reorder columns
        df_long = df_long[
            ["year", "period", "state", "category", "data_item", "value", "unit"]
        ]

        all_years.append(df_long)

    if not all_years:
        raise ValueError("No valid year sheets were parsed from this file.")

    final_df = pd.concat(all_years, ignore_index=True)
    return final_df


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Legacy COP Excel parser for old report-style COP files (e.g., 2005, 2010)."
    )
    parser.add_argument("--input", required=True, help="Path to legacy COP Excel file")
    parser.add_argument("--output", required=True, help="Path to save long-format CSV")
    args = parser.parse_args()

    df = parse_old_cop_excel(args.input)
    df.to_csv(args.output, index=False)
    print(f"Saved legacy COP long-format CSV → {args.output}")


if __name__ == "__main__":
    main()
