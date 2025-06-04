import os
from dotenv import load_dotenv
from LLM import LLM
from models import ToolEnum
from Tools import CalculatorUtils, WebSearchUtils
from Tools import CalculatorTool, WebSearchTool

load_dotenv()

async def send_response(user_prompt: str, tool: ToolEnum):
    try:
        # Get tool results (synchronously for now)
        if tool == ToolEnum.CALCULATOR:
            tool = CalculatorTool(CalculatorUtils())
        elif tool == ToolEnum.WEB_SEARCH:
            duckduckgo_api_key = os.getenv("DUCKDUCKGO_API_KEY")
            tool = WebSearchTool(WebSearchUtils(duckduckgo_api_key))
        
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