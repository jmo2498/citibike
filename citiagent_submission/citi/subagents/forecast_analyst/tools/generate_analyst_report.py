from ...forecast.tools.generate_report import generate_forecast_report
from .list_station_names import list_station_names
from .summarize_findings import summarize_forecast_findings

def generate_all_forecast_reports() -> str:
    try:
        station_names = list_station_names()
        entries = []

        for name in station_names:
            result = generate_forecast_report(name)
            if isinstance(result, dict):
                entries.append(result)

        summary = summarize_forecast_findings(entries)
        return summary

    except Exception as e:
        return f"❌ Failed to generate reports: {str(e)}"