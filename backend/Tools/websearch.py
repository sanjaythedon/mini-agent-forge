from serpapi import GoogleSearch


class WebSearchTool:
    def __init__(self, api_key: str):
        self.api_key = api_key
        
    def search(self, query: str):
        params = {
            "engine": "duckduckgo",
            "q": query,
            "kl": "us-en",
            "api_key": self.api_key
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