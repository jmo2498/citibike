from google.adk import Agent
from .prompt import FORECAST_AGENT_PROMPT
from .tools.generate_report import generate_forecast_report  # <- The actual function

MODEL = "gemini-2.0-flash"

forecast_agent = Agent(
    name="forecast_agent",
    model=MODEL,
    description=(
        "Reads in live data from Citi Bike stations and weather stations. "
        "When the user prompts for a station (e.g., 'Liberty St & Broadway'), "
        "returns the latest matching station data."
    ),
    instruction=FORECAST_AGENT_PROMPT,
    tools=[ generate_forecast_report
    ]
)