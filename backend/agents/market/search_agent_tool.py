from google.adk.agents import Agent
from google.adk.tools import google_search

# --- Specialist Agent for Google Search ---
# This agent is designed to be used as a tool by other agents.
# It is isolated in its own file to prevent import conflicts with the main agent.
search_agent = Agent(
    name="google_search_specialist",
    model="gemini-2.0-flash-001",
    description="A specialist agent that performs targeted Google searches for market news and sentiment. Takes a search query as input.",
    instruction="You are a search specialist. Given a query, use the google_search tool to find the most relevant news and market reports. Return a summary of the key findings.",
    tools=[google_search],
)
