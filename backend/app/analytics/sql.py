import pandas as pd
from backend.app.db.session import Engine

def fetch_dataframe(query: str) -> pd.DataFrame:
    """Run a SQL query and return a pandas DataFrame."""
    with Engine.connect() as conn:
        df = pd.read_sql(query, conn)
    return df
