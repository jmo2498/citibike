from google.adk import Agent
from .prompt import MONITOR_AGENT_PROMPT
from .tools.generate_reports import generate_station_report, generate_weather_report


MODEL = "gemini-2.0-flash"

monitor_agent = Agent(
    name="station_monitor_agent",
    model=MODEL,
    description=(
        "Monitoring agent that fetches Citi Bike station and weather data, "
        "flags low/surplus availability, and logs both reports to Firestore."
    ),
    instruction=MONITOR_AGENT_PROMPT,
    tools=[
        generate_station_report,
        generate_weather_report,
    ]  # <-- ADD THIS
)