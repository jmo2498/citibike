from datetime import datetime
import pandas as pd
from scripts.db import read_map, push_to_sql
from scripts.status import fetch_station_status_flat

def run_pipeline():
    map_df = read_map()
    if map_df.empty:
        return

    station_ids = map_df['station_id'].tolist()
    status_df = fetch_station_status_flat(station_ids)
    if status_df.empty:
        return

    status_df['last_reported'] = pd.to_datetime(status_df['last_reported'], unit='s')

    # ✅ Add pull timestamp
    status_df['retrieved_at'] = datetime.utcnow()

    merged_df = pd.merge(status_df, map_df, on='station_id', how='left')

    push_to_sql(merged_df)
