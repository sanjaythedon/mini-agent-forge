import os
from dotenv import load_dotenv
from models import ToolEnum
from Tools import CalculatorUtils, WebSearchUtils
from Tools import CalculatorTool, WebSearchTool

load_dotenv()


def generate_prompt_to_llm(user_prompt: str, tool: ToolEnum):
    try:
        # Get tool results (synchronously for now)
        if tool == ToolEnum.CALCULATOR:
            tool = CalculatorTool(CalculatorUtils())
        elif tool == ToolEnum.WEB_SEARCH:
            duckduckgo_api_key = os.getenv("DUCKDUCKGO_API_KEY")
            tool = WebSearchTool(WebSearchUtils(duckduckgo_api_key))

        results = tool.execute(user_prompt)

        system_prompt = tool.generate_prompt()

        response = {
            "system_prompt": system_prompt,
            "results": results
        }

        return response

    except Exception as e:
        print(f"Error in send_response: {e}")
        return f"Error: {str(e)}"