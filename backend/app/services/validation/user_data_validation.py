import os
import pandas as pd

SUPPORTED_EXTENSIONS = {".csv", ".xlsx", ".xls"}

def validate_uploaded_file(file_path: str):
    """
    Validates a user-uploaded FARM dataset file.
    Returns:
      - status: "ok" or "error"
      - errors: list of blocking issues
      - warnings: list of non-blocking issues
      - columns: list of detected columns
      - row_count: number of rows
    """

    errors = []
    warnings = []

    # ---------------------------
    # 1. Validate file extension
    # ---------------------------
    ext = os.path.splitext(file_path)[1].lower()
    if ext not in SUPPORTED_EXTENSIONS:
        return {
            "status": "error",
            "errors": [f"Unsupported file type: {ext}. Allowed: CSV, XLSX, XLS"],
            "warnings": []
        }

    # ---------------------------
    # 2. Validate file size
    # ---------------------------
    if os.path.getsize(file_path) == 0:
        return {
            "status": "error",
            "errors": ["The uploaded file is empty."],
            "warnings": []
        }

    # ---------------------------
    # 3. Try loading the file
    # ---------------------------
    try:
        if ext == ".csv":
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path)
    except Exception as e:
        return {
            "status": "error",
            "errors": [f"Could not read file: {str(e)}"],
            "warnings": []
        }

    # ---------------------------
    # 4. Validate dataframe shape
    # ---------------------------
    if df.empty:
        return {
            "status": "error",
            "errors": ["The file contains no rows."],
            "warnings": []
        }

    if df.shape[1] < 2:
        return {
            "status": "error",
            "errors": ["The file does not contain enough columns to be valid farm data."],
            "warnings": []
        }

    # ---------------------------
    # 5. Farm-data specific checks
    # ---------------------------

    # A. Check for a date column
    date_cols = [c for c in df.columns if "date" in c.lower()]
    if not date_cols:
        warnings.append("No date column detected. Time-series charts may not work.")

    # B. Check for numeric columns
    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
    if len(numeric_cols) == 0:
        warnings.append("No numeric columns detected. Charts may not render.")

    # C. Check for duplicate rows
    if df.duplicated().any():
        warnings.append("Duplicate rows detected. They will be removed during preprocessing.")

    # D. Check for empty columns
    empty_cols = [col for col in df.columns if df[col].isna().all()]
    if empty_cols:
        warnings.append(f"These columns are completely empty: {empty_cols}")

    # ---------------------------
    # 6. Return validation result
    # ---------------------------
    return {
        "status": "ok",
        "errors": errors,
        "warnings": warnings,
        "row_count": len(df),
        "columns": list(df.columns)
    }
