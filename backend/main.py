from google.adk.agents import Agent
from crop_disease_agent.agent import crop_agent
from govt_schemes_agent.agent import govt_agent
from market_insights_agent.agent import market_agent



# --- 3. Root agent (Delegating both tasks automatically) ---
root_agent = DelegatingAgent(
    delegates=[crop_agent, govt_agent,market_agent],
    instruction=(
        "You are a combined assistant. When the user asks for the price of an item, "
        "ALWAYS also provide the 10-day weather forecast for the same location by default. "
        "Return the price information first, followed by the weather forecast."
    ),
    model="gemini-2.0-flash"
)