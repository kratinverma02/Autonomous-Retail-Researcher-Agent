import os
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def search_web(query):
    response = tavily.search(
        query=query,
        max_results=8,
        search_depth="advanced"
    )
    return response.get("results", [])

