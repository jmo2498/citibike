import json
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from .get_cred import get_db_config
import logging

logging.basicConfig(level=logging.INFO)

def get_station_data(input: dict) -> dict:
    try:
        PG_CONN = get_db_config()
        db_url = f"mysql+pymysql://{PG_CONN['user']}:{PG_CONN['password']}@{PG_CONN['host']}:{PG_CONN['port']}/{PG_CONN['database']}"
        engine = create_engine(db_url)

        status_df = pd.read_sql("SELECT * FROM station_status_live_v2", engine)
        status_df['retrieved_at'] = pd.to_datetime(status_df['retrieved_at'])

        keep_cols = ["station_id", "name", "num_bikes_available", "num_docks_available", "retrieved_at", "lat", "lon"]
        status_df = status_df[keep_cols]

        status_df.sort_values(by=['station_id', 'retrieved_at'], ascending=[True, False], inplace=True)
        latest_df = status_df.drop_duplicates(subset='station_id', keep='first')

        latest_df = latest_df.replace({np.nan: None})
        latest_df = latest_df.dropna(subset=["station_id", "name", "num_bikes_available", "num_docks_available", "retrieved_at", "lat", "lon"])

        latest_df["num_bikes_available"] = latest_df["num_bikes_available"].astype(int)
        latest_df["num_docks_available"] = latest_df["num_docks_available"].astype(int)
        latest_df["station_id"] = latest_df["station_id"].astype(str)
        latest_df["name"] = latest_df["name"].astype(str)
        latest_df["retrieved_at"] = latest_df["retrieved_at"].astype(str)
        latest_df["lat"] = latest_df["lat"].astype(float)
        latest_df["lon"] = latest_df["lon"].astype(float)

        return {
            "status": "success",
            "stations": latest_df.to_dict(orient="records")
        }

    except Exception as e:
        logging.error("❌ Exception in get_station_data:", exc_info=True)
        return {
            "status": "error",
            "error_message": str(e)
        }