import os
import json
from datetime import datetime
from dotenv import load_dotenv
from LLM.llm import LLM
from models import ToolEnum
from Database import DatabaseOperations, DatabaseTableManager, DatabaseDataManager
from Database.connections import PostgresConnection
from redis_definition import Redis
from functions.calculator import calculator
from functions.duckduckgo import duckduckgo

load_dotenv()
redis = Redis()

def send_response(user_prompt: str, tool: ToolEnum):
    # cache = redis.get(user_prompt)
    # if cache:
    #     return cache   
    if tool == ToolEnum.CALCULATOR:
        results = calculator(user_prompt)
    elif tool == ToolEnum.WEB_SEARCH:
        results = duckduckgo(user_prompt)
    

    llm = LLM()
    
    if tool == ToolEnum.CALCULATOR:
        system_prompt = "You are a friendly assistant who helps with calculations. Present the user's calculation query along with its result in a clear, conversational way. Make your response concise but warm. Only use the information provided in the user's query and the calculation result."
    elif tool == ToolEnum.WEB_SEARCH:
        system_prompt = "You are a helpful assistant who provides web search results. Create a friendly response that lists all the search results with their titles and links in a well-formatted, easy-to-read manner. Start with a brief introduction acknowledging the user's search query, then present each result as a numbered list item with the title and clickable link. End with a brief, encouraging closing remark."
    
    prompt_to_llm = f"USER PROMPT:{user_prompt}\n\nTool: {tool}\n\nResponse: {results}"
    for response in llm.generate(prompt_to_llm, system_prompt):
        yield response
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
    
    return response