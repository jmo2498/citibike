
import pandas as pd
from sqlalchemy import create_engine
from google.cloud import secretmanager
import json

def get_db_config():
    client = secretmanager.SecretManagerServiceClient()
    secret_name = "projects/vertextraining-448821/secrets/sql_creds/versions/latest"
    response = client.access_secret_version(request={"name": secret_name})
    payload = response.payload.data.decode("utf-8")
    return json.loads(payload)


PG_CONN = get_db_config()

def read_map():
    try:
        db_url = f"mysql+pymysql://{PG_CONN['user']}:{PG_CONN['password']}@{PG_CONN['host']}:{PG_CONN['port']}/{PG_CONN['database']}"
        engine = create_engine(db_url)
        df = pd.read_sql("SELECT station_id, name, lat, lon FROM bike_stations;", engine)
        df['station_id'] = df['station_id'].astype(str)
        print(f"✅ Retrieved {len(df)} station metadata rows.")
        return df
    except Exception as e:
        print(f"❌ Failed to read map data: {e}")
        return pd.DataFrame()

def push_to_sql(df):
    try:
        db_url = f"mysql+pymysql://{PG_CONN['user']}:{PG_CONN['password']}@{PG_CONN['host']}:{PG_CONN['port']}/{PG_CONN['database']}"
        engine = create_engine(db_url)
        df.to_sql("station_status_live_v2", con=engine, if_exists="append", index=False)
        print("✅ Data pushed to MySQL.")
    except Exception as e:
        print(f"❌ Failed to push data to SQL: {e}")
