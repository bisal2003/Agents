# import datetime
# from google.adk.agents import Agent, LlmAgent, SequentialAgent
# from google.adk.tools import google_search
# import google.genai as genai
# from holiday import get_holidays
# from mandi import *

# def holiday():
#     return get_holidays(start_date=today,end_date=up to this month)
    
    
    
# news_agent = Agent(
#     name="google_search_specialist",
#     model="gemini-2.0-flash-001",
#     description="A specialist agent that performs targeted Google searches for market news and sentiment. Takes a search query as input specific to a location or area.",
#     instruction="You are a search specialist. Given a query, use the google_search tool to find the most relevant news and market reports. Return a summary of the key findings.",
#     tools=[google_search],
# )

# def mandi():
#     print("ok")
#     pass

# weather_agent = Agent(
#     name="weather_agent",
#     model="gemini-2.0-flash",
#     description="Provides the 10-day weather forecast for a specific location.",
#     instruction=(
#         "You are a weather assistant. When given a location, "
#         "use the 'google_search' tool to find the 10-day weather forecast. "
#         "Summarize temperature, rain chances, and extreme weather if any."
#     ),
#     tools=[google_search],
# )

# main_final_agent = SequentialAgent(
#     name="Final_agent_1",
#     sub_agents=[news_agent,weather_agent],
#     tools=[holiday,mandi],
#     discription='''You are a combined assistant. When the user asks for the price of an item, 
#        ALWAYS use the 10-day weather forecast for the same location by default. 
#        Analysis the holidays and local news also as that will help to know the upcoming demands of the items, say festival or wedding seasons.
#        Return the price information first, followed by the weather forecast.

# '''
# )

# # Root agent for app
# root_agent = main_final_agent


from datetime import datetime
from google.adk.agents import Agent, SequentialAgent
from google.adk.tools import google_search
from holiday import get_holidays
from mandi import fetch_mandi_data

def holiday_tool():
    """
    Returns holidays for the current month using Google Calendar API.
    """
    today = datetime.now()
    start_date = today.replace(day=1)
    # End date: first day of next month
    if start_date.month == 12:
        end_date = start_date.replace(year=start_date.year+1, month=1)
    else:
        end_date = start_date.replace(month=start_date.month+1)
    return get_holidays(start_date, end_date)

def mandi_tool(state: str = "Uttar Pradesh"):
    """
    Returns mandi price data for a given state.
    """
    return fetch_mandi_data(state)

news_agent = Agent(
    name="news_agent",
    model="gemini-2.0-flash-001",
    description="Provides market news and sentiment for a location or commodity.",
    instruction="You are a search specialist. Use the google_search tool to find relevant news and market reports. Return a summary of key findings.",
    tools=[google_search],
)

weather_agent = Agent(
    name="weather_agent",
    model="gemini-2.0-flash",
    description="Provides the 10-day weather forecast for a specific location.",
    instruction=(
        "You are a weather assistant. When given a location, "
        "use the 'google_search' tool to find the 10-day weather forecast. "
        "Summarize temperature, rain chances, and extreme weather if any."
    ),
    tools=[google_search],
)

main_final_agent = SequentialAgent(
    name="market_final_agent",
    sub_agents=[news_agent, weather_agent],
    tools=[holiday_tool, mandi_tool],
    description=(
        "You are a professional market analysis assistant. "
        "When the user asks for the price of an item, ALWAYS provide the 10-day weather forecast for the same location. "
        "Analyze holidays and local news to anticipate upcoming demand, such as festival or wedding seasons. "
        "Return price information first, followed by the weather forecast and relevant holiday/news analysis."
    ),
)

# Root agent for app
root_agent = main_final_agent