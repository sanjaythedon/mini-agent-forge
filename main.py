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
    elif tool == ToolEnum.DUCKDUCKGO:
        results = duckduckgo(user_prompt)

    llm = LLM()
    system_prompt = "You are a helpful assistant."
    prompt_to_llm = f"{user_prompt}\n\nTool: {tool}\n\nResponse: {results}"
    response = llm.generate(prompt_to_llm, system_prompt)

    connection_manager = PostgresConnection(
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        database=os.getenv("POSTGRES_DB")
    )
    table_manager = DatabaseTableManager(connection_manager)
    data_manager = DatabaseDataManager("%s", connection_manager)
    
    db = DatabaseOperations(
        connection_manager=connection_manager,
        table_manager=table_manager,
        data_manager=data_manager
    )
    columns = {
        "id": "SERIAL PRIMARY KEY",
        "timestamp": "TIMESTAMP",
        "prompt": "TEXT",
        "tool": "TEXT",
        "response": "TEXT"
    }
    db.create_table("prompt_log", columns)
    data = {
        "timestamp": datetime.now(),
        "prompt": user_prompt,
        "tool": tool.value,
        "response": response
    }
    db.insert("prompt_log", data)
    # print(db.read("prompt_log"))
    # redis.set(user_prompt, response)
    data['timestamp'] = data['timestamp'].isoformat()
    redis.push("user", json.dumps(data))
    redis.trim("user", 0, 9)
    print(redis.get_list("user"))
    
    return response