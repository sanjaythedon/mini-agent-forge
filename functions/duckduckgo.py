import os
from dotenv import load_dotenv
from serpapi import GoogleSearch

load_dotenv()

def duckduckgo(query: str):
    params = {
        "engine": "duckduckgo",
        "q": query,
        "kl": "us-en",
        "api_key": os.getenv("DUCKDUCKGO_API_KEY")  
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    res = []
    organic_results = results.get("organic_results")
    for result in organic_results:
        data = {
            'title': result.get("title"),
            'link': result.get("link")
        }
        res.append(data)
    return res