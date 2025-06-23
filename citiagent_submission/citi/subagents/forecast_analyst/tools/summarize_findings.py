from datetime import datetime

def summarize_forecast_findings(reports: list[dict]) -> str:
    summary = "# 📊 Forecast Analyst Summary\n\n"
    low_bikes, low_docks, balanced, errored = [], [], [], []

    for entry in reports:
        if "error" in entry:
            errored.append(entry["station"])
            continue

        station = entry.get("station", "Unknown Station")
        bikes = entry.get("bikes", 0)
        docks = entry.get("docks", 0)
        avg_trips = entry.get("avg_trips", 0)
        forecasted_trips = entry.get("forecasted_trips", 0)
        temp = entry.get("temperature", "N/A")
        cond = entry.get("condition", "N/A")
        risk_level = entry.get("risk_level", "")

        # Determine current time bucket
        current_hour = datetime.now().hour
        if current_hour < 12:
            time_bucket = "morning"
        elif current_hour < 17:
            time_bucket = "afternoon"
        else:
            time_bucket = "evening"

        avg_bucket_trip = entry.get("avg_trips_by_bucket", {}).get(time_bucket, 0)

        title = f"**{station}**"
        evidence = (
            f"  - {bikes} bikes, {docks} docks\n"
            f"  - {avg_bucket_trip:.1f} {time_bucket} trips, "
            f"{forecasted_trips:.1f} forecasted, {temp}°F, {cond}"
        )

        if risk_level == "low_bikes":
            summary += f"🚲 {title} (Low Bikes)\n{evidence}\n"
            low_bikes.append(entry)
        elif risk_level == "low_docks":
            summary += f"📦 {title} (Low Docks)\n{evidence}\n"
            low_docks.append(entry)
        elif risk_level == "balanced":
            summary += f"✅ {title} (Balanced)\n{evidence}\n"
            balanced.append(entry)

    summary += "\n---\n"
    summary += f"**Total Stations Checked:** {len(reports)}\n"
    summary += f"- 🚲 Low Bikes: {len(low_bikes)}\n"
    summary += f"- 📦 Low Docks: {len(low_docks)}\n"
    summary += f"- ✅ Balanced: {len(balanced)}\n"
    if errored:
        summary += f"- ⚠️ Errors: {len(errored)} ({', '.join(errored)})\n"

    summary += "\n## 🔁 Suggested Rebalancing Plan:\n"
    actions = []

    # Rebalance TO low bike stations FROM stations with excess bikes
    donors = sorted([s for s in balanced if s["bikes"] > 10], key=lambda s: s["bikes"], reverse=True)
    for receiver in low_bikes:
        for donor in donors:
            move_count = min(5, donor["bikes"] - 10, receiver["docks"] - 5)
            if move_count > 0:
                actions.append(f"Move {move_count} bikes from '{donor['station']}' to '{receiver['station']}'")
                donor["bikes"] -= move_count
                receiver["docks"] -= move_count
                break

    # Rebalance FROM low dock stations TO balanced stations with room
    recipients = sorted([s for s in balanced if s["docks"] > 5], key=lambda r: r["docks"], reverse=True)
    used_recipients = set()
    for full_station in low_docks:
        for recipient in recipients:
            if recipient["station"] in used_recipients:
                continue
            move_count = min(5, full_station["bikes"] - 10, recipient["docks"] - 5)
            if move_count > 0:
                actions.append(f"Move {move_count} bikes from '{full_station['station']}' to '{recipient['station']}'")
                full_station["bikes"] -= move_count
                recipient["docks"] -= move_count
                used_recipients.add(recipient["station"])
                break

    summary += "\n".join(actions) if actions else "No rebalancing actions required."
    summary += "\n\n_Generated using Firebase + BigQuery + live weather data._"

    return summary