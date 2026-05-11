import argparse
import pandas as pd
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text

from db import get_engine   # uses your existing DB engine


def parse_args():
    parser = argparse.ArgumentParser(description="Ingest long-format farm data into SQL")

    parser.add_argument("--file", required=True, help="Path to processed long-format CSV")
    parser.add_argument("--filename", required=False, help="Original uploaded filename")
    parser.add_argument("--dry-run", action="store_true", help="Validate but do not write to DB")

    return parser.parse_args()


def ingest_dataframe(df, filename, dry_run=False):
    engine = get_engine()
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()

    inserted = 0
    dataset_counts = {}

    insert_sql = text("""
        INSERT INTO farm_data_long (
            dataset_type,
            date,
            category,
            metric,
            value,
            uploaded_at,
            filename
        )
        VALUES (
            :dataset_type,
            :date,
            :category,
            :metric,
            :value,
            :uploaded_at,
            :filename
        );
    """)

    try:
        for _, row in df.iterrows():
            # dataset type comes from the CSV's category column
            row_dataset_type = row.get("category")

            # count rows per dataset type for logging
            dataset_counts[row_dataset_type] = dataset_counts.get(row_dataset_type, 0) + 1

            params = {
                "dataset_type": row_dataset_type,
                "date": row["date"],
                "category": None,  # optional category column (not dataset type)
                "metric": row["metric"],
                "value": float(row["value"]) if pd.notna(row["value"]) else None,
                "uploaded_at": datetime.utcnow(),
                "filename": filename
            }

            if not dry_run:
                session.execute(insert_sql, params)

            inserted += 1

        if not dry_run:
            session.commit()

        return inserted, dataset_counts

    except Exception as e:
        session.rollback()
        raise e

    finally:
        session.close()


def main():
    args = parse_args()

    print(f"\nLoading file: {args.file}")
    df = pd.read_csv(args.file)

    filename = args.filename if args.filename else args.file.split("/")[-1]

    print(f"Rows detected: {len(df)}")
    print("Beginning ingestion...\n")

    inserted, dataset_counts = ingest_dataframe(
        df=df,
        filename=filename,
        dry_run=args.dry_run
    )

    print("Ingestion complete.")
    print(f"Total rows processed: {inserted}")

    print("\nRows per dataset type:")
    for dtype, count in dataset_counts.items():
        print(f"  {dtype}: {count}")

    if args.dry_run:
        print("\nDry run mode — no rows written to database.")
    else:
        print("\nRows successfully written to database.")


if __name__ == "__main__":
    main()
