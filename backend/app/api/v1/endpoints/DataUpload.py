from fastapi import APIRouter, UploadFile, File, Form
import os
import pandas as pd
import subprocess
import sys

router = APIRouter()

UPLOAD_DIR = "uploads/raw"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Absolute path to ingestion script
INGEST_SCRIPT = os.path.abspath("ingestion/ingestion_py/user_sql_ingestion.py")


@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    customer_id: str = Form(...)   # NEW FIELD
):
    print("HIT /upload ROUTE")  # sanity check
    print("Customer ID:", customer_id)

    # 1. Save raw file
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    # 2. Validate load
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        return {
            "status": "error",
            "message": f"Could not load file: {str(e)}"
        }

    # 3. Run ingestion script with absolute path + correct Python interpreter
    try:
        result = subprocess.run(
            [
                sys.executable,
                INGEST_SCRIPT,
                "--file", file_path,
                "--customer_id", customer_id   # PASS TO INGESTION SCRIPT
            ],
            capture_output=True,
            text=True
        )

        # Log stderr/stdout to FastAPI console
        if result.returncode != 0:
            print("\n================ INGESTION ERROR ================\n")
            print("Return code:", result.returncode)
            print("STDERR:", result.stderr)
            print("STDOUT:", result.stdout)
            print("Script path:", INGEST_SCRIPT)
            print("\n=================================================\n")

            return {
                "status": "error",
                "message": "Ingestion script failed",
                "details": result.stderr or result.stdout
            }

    except Exception as e:
        print("\n================ INGESTION EXCEPTION ================\n")
        print(str(e))
        print("\n=====================================================\n")

        return {
            "status": "error",
            "message": f"Ingestion failed: {str(e)}"
        }

    # 4. Success
    return {
        "status": "ok",
        "message": "File uploaded and processed successfully",
        "customer_id": customer_id,
        "script_output": result.stdout
    }
