from LLM.llm import LLM
from models import ToolEnum
from functions.calculator import calculator
from functions.duckduckgo import duckduckgo

def send_response(user_prompt: str, tool: ToolEnum):
    if tool == ToolEnum.CALCULATOR:
        results = calculator(user_prompt)
    elif tool == ToolEnum.DUCKDUCKGO:
        results = duckduckgo(user_prompt)

    llm = LLM()
    system_prompt = "You are a helpful assistant."
    user_prompt = f"{user_prompt}\n\nTool: {tool}\n\nResponse: {results}"
    response = llm.generate(user_prompt, system_prompt)
    
    return response