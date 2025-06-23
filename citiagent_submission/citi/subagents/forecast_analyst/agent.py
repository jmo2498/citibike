from google.adk import Agent
from .prompt import FORECAST_ANALYST_PROMPT
from .tools.generate_analyst_report import generate_all_forecast_reports  # <- The actual function

MODEL = "gemini-2.0-flash"

forecast_analyst_agent = Agent(
    name="forecast_analyst_agent",
    model=MODEL,
    description=(
        "Evaluates all Citi Bike stations using live status and weather data, along with historical demand. "
        "Returns a summary of high-risk, surplus, or balanced stations across the network."
    ),
    instruction=FORECAST_ANALYST_PROMPT,
    tools=[generate_all_forecast_reports
    ]
)