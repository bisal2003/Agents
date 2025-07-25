from google.adk.tools import tool

from google.adk.tools import google_search


@tool(
    name="get_10_day_weather_forecast",
    description="Gets the 10-day weather forecast for a given location.",
)
def get_10_day_weather_forecast(location: str) -> str:
    """
    This tool takes a location and returns the 10-day weather forecast.
    """
    return google_search.run(f"10 day weather forecast for {location}")
