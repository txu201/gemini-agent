from google.adk.agents import Agent
from google.adk.tools import google_search

agent_search = Agent(
    name="AgentSearch",
    model="gemini-2.0-flash",
    instruction="Answer any general query using the google_search tool.",
    tools=[google_search],
    description="Agent that answers using Google search only."
)