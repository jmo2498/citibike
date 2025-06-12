import json
import pandas as pd
import datetime
from sqlalchemy import create_engine
from .get_cred import get_db_config

def get_weather(input: dict) -> dict:
    try:
        # Connect to DB
        PG_CONN = get_db_config()
        db_url = (
            f"mysql+pymysql://{PG_CONN['user']}:{PG_CONN['password']}@"
            f"{PG_CONN['host']}:{PG_CONN['port']}/{PG_CONN['database']}"
        )
        engine = create_engine(db_url)

        # Load the full table
        df = pd.read_sql("SELECT * FROM weather_live", engine)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        latest = df.sort_values(by='timestamp', ascending=False).iloc[0]

        # Ensure native types
        report = {
            "temperature_c": float(latest["temperature_c"]),
            "feels_like_c": float(latest["feels_like_c"]),
            "humidity_percent": int(latest["humidity_percent"]),
            "wind_speed_mps": float(latest["wind_speed_mps"]),
            "description": str(latest["description"]),
            "condition": str(latest["condition"]),
            "timestamp": latest["timestamp"].isoformat()
        }

        return {"status": "success", "report": report}

    except Exception as e:
        return {"status": "error", "error_message": str(e)}
