import os
import json
import pandas as pd
from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from .subagents.monitor import monitor_agent



root_agent = Agent(
    name="root_agent",
    model="gemini-2.0-flash",
    description=(
        "The root agent coordinates all sub-agents to ensure optimal monitoring, forecasting, reporting, and decision-making "
        "for Citi Bike station availability."
    ),
    instruction=(
        "You are the root agent responsible for coordinating other agents in the Citi Bike monitoring system.\n\n"
        "Your main responsibilities include:\n"
        "- Calling the `monitor_agent` to collect station status data.\n"
        "- Storing and organizing data from the monitor agent to prepare it for use by forecasting and reporting agents.\n"
        "- Keeping track of which agents have been run and when.\n\n"
        "At this stage, your task is to run the `monitor_agent` and return its output in full. Do not summarize or modify the output.\n"
        "This output will later be used by downstream agents like the forecast and decision agents."
    ),
    tools=[AgentTool(agent=monitor_agent)],

)