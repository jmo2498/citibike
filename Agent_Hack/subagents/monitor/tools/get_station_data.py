import json
import pandas as pd
import datetime  # Added for timestamp handling
from sqlalchemy import create_engine
from .get_cred import get_db_config
# -----------------------------

def get_station_data(input: dict) -> dict:
    try:
        PG_CONN = get_db_config()
        db_url = f"mysql+pymysql://{PG_CONN['user']}:{PG_CONN['password']}@{PG_CONN['host']}:{PG_CONN['port']}/{PG_CONN['database']}"
        engine = create_engine(db_url)

        # Load the full status table
        status_df = pd.read_sql("SELECT * FROM station_status_live_v2", engine)

        # Convert timestamp and filter latest per station
        status_df['retrieved_at'] = pd.to_datetime(status_df['retrieved_at'])
        status_df.sort_values(by=['station_id', 'retrieved_at'], ascending=[True, False], inplace=True)
        latest_df = status_df.drop_duplicates(subset='station_id', keep='first')

        # Convert to dict
        return {
            "status": "success",
            "stations": latest_df.to_dict(orient="records")
        }

    except Exception as e:
        return {
            "status": "error",
            "error_message": str(e)
        }
