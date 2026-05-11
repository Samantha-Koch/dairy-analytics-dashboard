import pandas as pd
from datetime import datetime

def preprocess_dataset(dataset_type: str, df: pd.DataFrame):
    """
    Cleans and standardizes user-uploaded FARM data.
    Converts all datasets to LONG FORMAT.
    Returns:
      - dataset_type
      - records (list of dicts)
      - preview (first 5 rows)
      - row_count
    """

    df = df.copy()

    # ---------------------------
    # 1. Normalize column names
    # ---------------------------
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("-", "_")
        .str.replace(r"[^a-zA-Z0-9_]", "", regex=True)
    )

    # ---------------------------
    # 2. Parse date columns
    # ---------------------------
    date_col = None
    for col in df.columns:
        if "date" in col:
            df[col] = pd.to_datetime(df[col], errors="coerce")
            date_col = col
            break

    if date_col is None:
        # Create a placeholder date column if missing
        df["date"] = pd.NaT
        date_col = "date"

    # ---------------------------
    # 3. Convert numeric columns
    # ---------------------------
    for col in df.columns:
        if df[col].dtype == object:
            df[col] = (
                df[col]
                .astype(str)
                .str.replace(",", "")
                .str.replace("$", "")
                .str.replace(" ", "")
            )
            df[col] = pd.to_numeric(df[col], errors="ignore")

    # ---------------------------
    # 4. Remove duplicates
    # ---------------------------
    df = df.drop_duplicates()

    # ---------------------------
    # 5. Dataset-specific cleaning
    # ---------------------------
    if dataset_type == "production":
        df = _clean_production_data(df)

    elif dataset_type == "feed":
        df = _clean_feed_data(df)

    elif dataset_type == "herd_health":
        df = _clean_herd_health_data(df)

    elif dataset_type == "financial":
        df = _clean_financial_data(df)

    # ---------------------------
    # 6. Convert to LONG FORMAT
    # ---------------------------
    long_df = _reshape_to_long(df, dataset_type, date_col)

    # ---------------------------
    # 7. Build return structure
    # ---------------------------
    preview = long_df.head(5).to_dict(orient="records")
    records = long_df.to_dict(orient="records")

    return {
        "dataset_type": dataset_type,
        "records": records,
        "preview": preview,
        "row_count": len(long_df)
    }


# ============================================================
#   DATASET-SPECIFIC CLEANERS
# ============================================================

def _clean_production_data(df: pd.DataFrame):
    """Standardize production dataset fields."""
    return df


def _clean_feed_data(df: pd.DataFrame):
    """Standardize feed dataset fields."""
    return df


def _clean_herd_health_data(df: pd.DataFrame):
    """Standardize mastitis + dry period dataset fields."""
    return df


def _clean_financial_data(df: pd.DataFrame):
    """Standardize financial dataset fields."""
    return df


# ============================================================
#   LONG FORMAT RESHAPE
# ============================================================

def _reshape_to_long(df: pd.DataFrame, dataset_type: str, date_col: str):
    """
    Converts any farm dataset into long format.
    Output columns:
      - date
      - metric
      - value
      - (optional category)
    """

    id_vars = [date_col]

    # Feed data keeps feed_type as a category
    if dataset_type == "feed" and "feed_type" in df.columns:
        id_vars.append("feed_type")

    value_vars = [c for c in df.columns if c not in id_vars]

    long_df = df.melt(
        id_vars=id_vars,
        value_vars=value_vars,
        var_name="metric",
        value_name="value"
    )

    # Drop rows where value is empty
    long_df = long_df.dropna(subset=["value"], how="all")

    return long_df
