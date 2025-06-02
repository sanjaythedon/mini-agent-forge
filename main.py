import os
from datetime import datetime
from dotenv import load_dotenv
from LLM.llm import LLM
from models import ToolEnum
from Database import DatabaseOperations, DatabaseTableManager, DatabaseDataManager
from Database.connections import PostgresConnection
from functions.calculator import calculator
from functions.duckduckgo import duckduckgo

load_dotenv()

def send_response(user_prompt: str, tool: ToolEnum):
    if tool == ToolEnum.CALCULATOR:
        results = calculator(user_prompt)
    elif tool == ToolEnum.DUCKDUCKGO:
        results = duckduckgo(user_prompt)

    llm = LLM()
    system_prompt = "You are a helpful assistant."
    user_prompt = f"{user_prompt}\n\nTool: {tool}\n\nResponse: {results}"
    response = llm.generate(user_prompt, system_prompt)

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
    print("tool: ", tool)
    db.insert("prompt_log", {"timestamp": datetime.now(), "prompt": user_prompt, "tool": tool.value, "response": response})
    print(db.read("prompt_log"))
    
    return response