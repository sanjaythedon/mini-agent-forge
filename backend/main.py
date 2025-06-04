import os
import json
from datetime import datetime
from dotenv import load_dotenv
from LLM import LLM
from models import ToolEnum
from Database import DatabaseOperations, DatabaseTableManager, DatabaseDataManager
from Database.connections import PostgresConnection
from Redis import Redis
from Tools import Calculator
from Tools import WebSearch
from Tools.interfaces import CalculatorTool, WebSearchTool

load_dotenv()
redis = Redis(
    host=os.getenv("REDIS_HOST"),
    port=os.getenv("REDIS_PORT"),
    db=os.getenv("REDIS_DB")
)

async def send_response(user_prompt: str, tool: ToolEnum):
    try:
        # Get tool results (synchronously for now)
        if tool == ToolEnum.CALCULATOR:
            tool = CalculatorTool(Calculator())
        elif tool == ToolEnum.WEB_SEARCH:
            duckduckgo_api_key = os.getenv("DUCKDUCKGO_API_KEY")
            tool = WebSearchTool(WebSearch(duckduckgo_api_key))
        
        # Initialize LLM
        llm = LLM()

        results = tool.execute(user_prompt)
        
        system_prompt = tool.generate_prompt()
        prompt_to_llm = f"USER PROMPT:{user_prompt}\n\nResponse: {results}"
        
        # Stream the response asynchronously
        async for chunk in llm.generate_stream(prompt_to_llm, system_prompt):
            yield chunk
            
    except Exception as e:
        print(f"Error in send_response: {e}")
        yield f"Error: {str(e)}"