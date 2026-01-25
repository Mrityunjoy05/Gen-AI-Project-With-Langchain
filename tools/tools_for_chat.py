from tools.tavily_search import TavilySearchTool
from langchain_core.tools import tool
from config.settings import settings
import requests
import os

# Initialize search tools (module level)
_tavily_search = TavilySearchTool()


@tool
def search_web_tavily(query: str) -> str:
    """
    Search the web using Tavily for comprehensive results.
    
    Use this when you need detailed information from the internet.
    
    Args:
        query: The search query string
    """
    try:
        result = _tavily_search.search(query)
        return result
    except Exception as e:
        return f"Error searching Tavily: {str(e)}"


@tool
def calculate(expression: str) -> str:
    """
    Evaluate a mathematical expression.
    
    Use this to perform calculations.
    
    Args:
        expression: Mathematical expression to evaluate (e.g., "2 + 2", "10 * 5")
        
    Returns:
        Result of the calculation
    """
    try:
        # Safe evaluation
        result = eval(expression, {"__builtins__": {}}, {})
        return str(result)
    except Exception as e:
        return f"Error calculating: {str(e)}"


@tool
def get_weather(city: str) -> str:
    """
    Get current weather for a city.
    
    Args:
        city: City name (e.g., 'London', 'Mumbai', 'New York')
    """
    api_key = settings.OPENWEATHER_API_KEY
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    
    try:
        params = {
            'q': city,              # City name method (easier)
            'appid': api_key,
            'units': 'metric'       # Celsius (most common globally)
        }
        
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        return str({
            'city': data['name'],
            'country': data['sys']['country'],
            'temperature': f"{data['main']['temp']}°C",  # Shows: 8.5°C
            'feels_like': f"{data['main']['feels_like']}°C",
            'conditions': data['weather'][0]['description'],
            'humidity': f"{data['main']['humidity']}%",
            'wind_speed': f"{data['wind']['speed']} m/s"
        })
        
    except Exception as e:
        return f"Error: {str(e)}"
# Export all tools
def get_all_tools():
    """Get list of all available tools."""
    return [
        search_web_tavily,
        get_weather,
        calculate
    ]