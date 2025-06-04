import os
import json
from datetime import datetime
from dotenv import load_dotenv
from LLM import LLM
from models import ToolEnum
from Database import DatabaseOperations, DatabaseTableManager, DatabaseDataManager
from Database.connections import PostgresConnection
from redis_definition import Redis
from functions.calculator import calculator
from functions.duckduckgo import duckduckgo

load_dotenv()
redis = Redis()

async def send_response(user_prompt: str, tool: ToolEnum):
    try:
        # Get tool results (synchronously for now)
        if tool == ToolEnum.CALCULATOR:
            results = calculator(user_prompt)
        elif tool == ToolEnum.WEB_SEARCH:
            results = duckduckgo(user_prompt)
        else:
            results = ""
        
        # Initialize LLM
        llm = LLM()
        
        # Set appropriate system prompt
        if tool == ToolEnum.CALCULATOR:
            system_prompt = """You are a friendly assistant who helps with calculations. Present the user's calculation query along with its result in a clear, conversational way. 
            
IMPORTANT: 
- Use plain text with standard math operators (+, -, *, /, ^, etc.)
- DO NOT use any LaTeX math delimiters (like $ or $$)
- DO NOT use markdown formatting
- Keep the response concise but warm
- Only use the information provided in the user's query and the calculation result"""
        elif tool == ToolEnum.WEB_SEARCH:
            system_prompt = """You are a helpful assistant who provides web search results. Generate an HTML-formatted response that lists all search results with proper styling.

Format your response as follows:
1. Start with a header element containing a friendly reply for the search query
2. Create a numbered list of results where each item contains:
   - The title in bold
   - The URL as a clickable link
3. End with a closing remark in a paragraph

Example format:
<header><h2>Some friendly reply about the query:</h2></header>
<ol>
  <li><strong>Title 1</strong><br><a href="https://example1.com">https://example1.com</a></li>
  <li><strong>Title 2</strong><br><a href="https://example2.com">https://example2.com</a></li>
</ol>
<p>Some closing remark about the query.</p>

Make sure to:
- Use proper HTML escaping for special characters
- Include the full URL in the link text
- Keep the response clean and well-formatted"""
        else:
            system_prompt = "You are a helpful assistant."
        
        # Prepare the prompt for LLM
        prompt_to_llm = f"USER PROMPT:{user_prompt}\n\nTool: {tool}\n\nResponse: {results}"
        
        # Stream the response asynchronously
        async for chunk in llm.generate_stream(prompt_to_llm, system_prompt):
            yield chunk
            
    except Exception as e:
        print(f"Error in send_response: {e}")
        yield f"Error: {str(e)}"
    # response = llm.generate(prompt_to_llm, system_prompt)

    # connection_manager = PostgresConnection(
    #     host=os.getenv("POSTGRES_HOST"),
    #     port=os.getenv("POSTGRES_PORT"),
    #     user=os.getenv("POSTGRES_USER"),
    #     password=os.getenv("POSTGRES_PASSWORD"),
    #     database=os.getenv("POSTGRES_DB")
    # )
    # table_manager = DatabaseTableManager(connection_manager)
    # data_manager = DatabaseDataManager("%s", connection_manager)
    
    # db = DatabaseOperations(
    #     connection_manager=connection_manager,
    #     table_manager=table_manager,
    #     data_manager=data_manager
    # )
    # columns = {
    #     "id": "SERIAL PRIMARY KEY",
    #     "timestamp": "TIMESTAMP",
    #     "prompt": "TEXT",
    #     "tool": "TEXT",
    #     "response": "TEXT"
    # }
    # db.create_table("prompt_log", columns)
    # data = {
    #     "timestamp": datetime.now(),
    #     "prompt": user_prompt,
    #     "tool": tool.value,
    #     "response": response
    # }
    # db.insert("prompt_log", data)
    # # print(db.read("prompt_log"))
    # # redis.set(user_prompt, response)
    # data['timestamp'] = data['timestamp'].isoformat()
    # redis.push("user", json.dumps(data))
    # redis.trim("user", 0, 9)
    # print(redis.get_list("user"))
    
    # return response