import os
import requests
import subprocess
import pandas as pd
from urllib.parse import quote
from ingestion.ingestion_py.db import get_engine

BASE_URL = "https://mpr.datamart.ams.usda.gov/services/v1.1/reports"

RAW_DIR = "ingestion/preprocessing/raw"
PROCESSED_DIR = "ingestion/preprocessing/processed"

REPORTS = {
    "class_prices_by_order": {
        "id": 3355,
        "sections": [
            "Final Class Prices by Order",
        ],
    },
    "producer_milk_components": {
        "id": 3462,
        "sections": [
            "Receipts",
            "Butterfat",
            "NFS",
            "Protein",
            "Other Solids",
            "SomCell",
        ],
    },
}


def ensure_dirs():
    os.makedirs(RAW_DIR, exist_ok=True)
    os.makedirs(PROCESSED_DIR, exist_ok=True)


def fetch_section_data(report_id, section_name):
    # URL‑encode section name (spaces, etc.)
    section_encoded = quote(section_name, safe="")
    url = f"{BASE_URL}/{report_id}/{section_encoded}"
    r = requests.get(url)
    r.raise_for_status()
    return r.json()


def save_raw_csv(report_key, section_name, data):
    if not data:
        return None

    safe_section = section_name.replace(" ", "_")
    filename = f"{report_key}_{safe_section}_raw.csv"
    path = os.path.join(RAW_DIR, filename)

    df = pd.json_normalize(data)
    df.to_csv(path, index=False)
    return path


def run_preprocessing(raw_path):
    processed_path = os.path.join(
        PROCESSED_DIR,
        os.path.basename(raw_path).replace("_raw.csv", "_long.csv"),
    )

    cmd = [
        "python",
        "ingestion/preprocessing/reshape_usda.py",
        "--input",
        raw_path,
        "--output",
        processed_path,
    ]
    subprocess.run(cmd, check=True)
    return processed_path


def run_ingestion(processed_path, report_key, section_name):
    safe_section = section_name.replace(" ", "_")
    slug = f"lmprs_{report_key}_{safe_section}"
    dataset_name = f"LMPRS {report_key.replace('_', ' ').title()} – {section_name}"

    cmd = [
        "python",
        "-m","ingestion.ingestion_py.ingest_usda_long_csv",
        "--dataset-slug",
        slug,
        "--dataset-name",
        dataset_name,
        "--csv",
        processed_path,
    ]
    subprocess.run(cmd, check=True)


def main():
    ensure_dirs()

    for report_key, cfg in REPORTS.items():
        report_id = cfg["id"]
        sections = cfg["sections"]

        print(f"\n=== Fetching report {report_key} ({report_id}) ===")

        for section_name in sections:
            print(f"\n→ Fetching section: {section_name}")
            try:
                data = fetch_section_data(report_id, section_name)
                raw_path = save_raw_csv(report_key, section_name, data)

                if raw_path is None:
                    print(f"   (No data returned for {section_name})")
                    continue

                print(f"   Saved raw → {raw_path}")

                processed_path = run_preprocessing(raw_path)
                print(f"   Processed → {processed_path}")

                run_ingestion(processed_path, report_key, section_name)
                print(f"   Ingested → {section_name}")

            except Exception as e:
                print(f"   ERROR in section {section_name}: {e}")

    print("\n=== COMPLETE ===")


if __name__ == "__main__":
    main()
