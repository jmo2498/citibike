from .read_firebase import read_firebase_variables
from .pull_big_query import query_trip_volume
from .forecast_demand import forecast_demand
import pandas as pd

def generate_forecast_report(station_name: str) -> dict:
    meta = read_firebase_variables(station_name)
    if "error" in meta:
        return {
            "station": station_name,
            "error": meta["error"]
        }

    trip_data_raw = query_trip_volume(meta["lat"], meta["lon"], meta["temperature"])
    if not trip_data_raw:
        return {
            "station": station_name,
            "error": "No historical trip data available for this station."
        }

    trip_df = pd.DataFrame(trip_data_raw)

    # Thresholds
    HIGH_TRIP_THRESHOLD = 550
    LOW_TRIP_THRESHOLD = 250

    # Metrics
    bikes = int(meta.get("bikes", 0))
    docks = int(meta.get("docks", 0))
    temp_f = float(meta["temperature"])
    total_capacity = bikes + docks
    utilization = bikes / total_capacity if total_capacity > 0 else 0.0

    # Cleaned up average trip volume by time bucket
    avg_by_bucket = {
        k: float(v)
        for k, v in trip_df.groupby("time_bucket")["trip_count"].mean().to_dict().items()
    }

    # Forecasted trips using all time buckets
    forecasted_trips = float(forecast_demand(trip_df))

    # Identify dominant time bucket
    most_active_bucket = max(avg_by_bucket.items(), key=lambda x: x[1])[0].capitalize()

    daily_avg = float(trip_df.groupby("trip_date")["trip_count"].sum().mean())

    # Risk logic
    if bikes == 0:
        risk = "Low Bikes: No bikes available. Needs urgent rebalancing."
        risk_level = "low_bikes"
    elif docks == 0:
        risk = "Low Docks: No docks available. Needs urgent rebalancing."
        risk_level = "low_docks"
    elif utilization < 0.2 and forecasted_trips > HIGH_TRIP_THRESHOLD:
        risk = f"Low Bikes: Risk of running out during {most_active_bucket.lower()} due to high forecasted demand."
        risk_level = "low_bikes"
    elif utilization > 0.8 and forecasted_trips > HIGH_TRIP_THRESHOLD:
        risk = f"Low Docks: Risk of reaching full capacity during {most_active_bucket.lower()} due to high forecasted usage."
        risk_level = "low_docks"
    else:
        risk = "Balanced: Bikes and docks match expected demand."
        risk_level = "balanced"

    # Markdown report
    report = f"""# Forecast Report for {station_name}

##  Station Status
- Bikes: {bikes}
- Docks: {docks}
- Flag: {meta['flag']}

##  Weather
- Condition: {meta['condition']}
- Temperature: {temp_f}°F
- Wind: {meta['wind']} m/s
- Humidity: {meta['humidity']}%

- Avg Trips (Morning): {avg_by_bucket.get('morning', 0.0):.1f}
- Avg Trips (Afternoon): {avg_by_bucket.get('afternoon', 0.0):.1f}
- Avg Trips (Evening): {avg_by_bucket.get('evening', 0.0):.1f}
- Forecasted Trips (Next Time Bucket): {forecasted_trips:.1f}
- Peak Usage Period: {most_active_bucket}
- Forecast Summary: {risk}
## 📈 History Sample
"""

    for row in trip_df.head(5).to_dict(orient="records"):
        date_str = str(row["trip_date"])
        report += (
            f"- {date_str} [{row['time_bucket']}]: {int(row['trip_count'])} trips @ {float(row['temperature']):.1f}°F\n"
        )

    report += "\n_Generated using Firebase + BigQuery data_\n"

    summary = (
        f"{bikes} bikes, {docks} docks. Temp {temp_f}°F, {meta['condition']}. "
        f"Avg. {daily_avg:.0f} daily trips. Forecast: {forecasted_trips:.0f} trips for the upcoming {most_active_bucket.lower()}. "
    )
    if risk_level != "balanced":
        summary += f" {risk} Recommend rebalancing."
    else:
        summary += risk

    return {
        "station": station_name,
        "bikes": bikes,
        "docks": docks,
        "avg_trips": daily_avg,
        "avg_trips_by_bucket": avg_by_bucket,
        "forecasted_trips": forecasted_trips,
        "temperature": temp_f,
        "condition": meta["condition"],
        "flag": meta["flag"],
        "risk": risk,
        "risk_level": risk_level,
        "report": report,
        "summary": summary
    }