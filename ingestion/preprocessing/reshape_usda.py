import pandas as pd
import os
import argparse

def load_file(path: str) -> pd.DataFrame:
    ext = os.path.splitext(path)[1].lower()
    if ext in [".xls", ".xlsx"]:
        return pd.read_excel(path)
    elif ext == ".csv":
        return pd.read_csv(path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")

def is_long_format(df: pd.DataFrame) -> bool: 
    cols = set(df.columns.str.lower())
    return (
        "value" in cols and 
        ("item" in cols or "data_item" in cols) and
        "year" in cols
    )

def reshape_wide_to_long(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = [c.strip().lower().replace(" ", "_").replace("-", "_") for c in df.columns]
    if "report_year" in df.columns:
        df["year"] = df["report_year"]
    if "period" in df.columns:
            df["period"] = df["period"].astype(str).replace("-", "_").str.upper()
    elif "report_month" in df.columns:
            df["period"] = df["report_month"].str[:3].str.upper()
    else:
            df["period"] = "annual"
    id_cols = []

    for c in ["state", "region", "year", "country", "size", "period"]:
        if c in df.columns:
            id_cols.append(c)
    value_cols = [c for c in df.columns if c not in id_cols]

    df_long = df.melt(
        id_vars=id_cols,
        value_vars=value_cols,
        var_name="data_item",
        value_name="value"
    )

    df_long["category"] = "cop_state"
    df_long["unit"] = None
    return df_long

def reshape_long_format(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

    if "period" not in df.columns:
        df["period"] = "annual"
    if "category" not in df.columns:
        df["category"] = None
    if "unit" not in df.columns and "units" in df.columns:
        df["unit"] = df["units"]

    return df

def reshape_usda(input_path: str, output_path: str):
    df = load_file(input_path)

    if is_long_format(df):
        df_out = reshape_long_format(df)
    else:
        df_out = reshape_wide_to_long(df)

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