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
    return results