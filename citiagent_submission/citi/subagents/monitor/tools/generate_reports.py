from .firebase_writer import write_monitor_report
from .get_station_data import get_station_data
from .get_weather import get_weather
from datetime import datetime

def generate_station_report(_: dict) -> dict:
    # 1) fetch raw data
    resp = get_station_data({"limit": 1_000_000})
    if resp["status"] != "success":
        return {"status":"error","error":"couldn't fetch station data"}
    stations = []
    for s in resp["stations"]:
        bikes = s["num_bikes_available"]
        docks = s["num_docks_available"]
        cap   = bikes + docks
        if not isinstance(bikes, int) or not isinstance(docks, int) or cap == 0:
            continue
        pct = bikes / cap * 100
        if pct <= 10:
            flag = "low_bike_availability"
        elif pct >= 90:
            flag = "surplus_bike_availability"
        else:
            flag = "normal"
        stations.append({
            **s,
            "flag": flag
        })
    payload = {
        "report": {
            "stations": stations,
            "timestamp": datetime.utcnow().isoformat()
        }
    }
    return write_monitor_report(header="stations", data=payload)

def generate_weather_report(_: dict) -> dict:
    resp = get_weather({})
    if resp["status"] != "success":
        return {"status":"error","error":"couldn't fetch weather"}
    payload = {
        "report": {
            "weather": resp["report"]
        }
    }
    return write_monitor_report(header="weather", data=payload)