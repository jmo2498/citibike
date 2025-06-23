import json
import pandas as pd
import datetime
import logging
from sqlalchemy import create_engine
from .get_cred import get_db_config

# Configure logging
logging.basicConfig(level=logging.INFO)

def get_weather(input: dict) -> dict:
    try:
        logging.info("🌤️ Starting get_weather()")

        # Connect to DB
        PG_CONN = get_db_config()
        db_url = (
            f"mysql+pymysql://{PG_CONN['user']}:{PG_CONN['password']}@"
            f"{PG_CONN['host']}:{PG_CONN['port']}/{PG_CONN['database']}"
        )
        logging.info(f"🔌 Connecting to DB: {PG_CONN['host']}")
        engine = create_engine(db_url)

        # Load the full table
        logging.info("📥 Querying weather_live table")
        df = pd.read_sql("SELECT * FROM weather_live", engine)
        df['timestamp'] = pd.to_datetime(df['timestamp'])

        latest = df.sort_values(by='timestamp', ascending=False).iloc[0]
        logging.info(f"📊 Latest weather timestamp: {latest['timestamp']}")

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

        logging.info("✅ Weather data retrieved successfully")
        return {"status": "success", "report": report}

    except Exception as e:
        logging.error("❌ Failed in get_weather()", exc_info=True)
        return {"status": "error", "error_message": str(e)}
