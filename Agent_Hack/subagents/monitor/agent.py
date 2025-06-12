from google.adk import Agent
from .tools.get_cred import get_db_config
from .tools.get_station_data import get_station_data
from .tools.get_weather import get_weather
from . import prompt

MODEL = "gemini-2.0-flash"

monitor_agent = Agent(
    name="station_monitor_agent",
    model=MODEL,
    description=(
        "Monitoring agent that fetches the most recent data for each unique Citi Bike station, "
        "returning number of bikes available and number of docks available with a status flag."
    ),
    instruction= prompt.MONITOR_AGENT_PROMPT,

    tools=[get_db_config, get_station_data, get_weather]

)
