from google.adk.agents import Agent
from .agent import audit_versioning_agent

def run(events: list):
    # Passes the event history (auto-handled by ADK)
    return audit_versioning_agent.run(input=events)


