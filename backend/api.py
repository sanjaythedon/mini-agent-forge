import json
import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from main import send_response
from fastapi.websockets import WebSocket
from models import Payload, ToolEnum
from Database.connections import PostgresConnection
from Database.operations import DatabaseOperations, DatabaseTableManager, DatabaseDataManager
from Redis import Redis
from datetime import datetime
import os
from dotenv import load_dotenv
load_dotenv()

redis = Redis(
    host=os.getenv("REDIS_HOST"),
    port=os.getenv("REDIS_PORT"),
    db=os.getnv("REDIS_DB")
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Hello World"}


@app.get("/chat-history")
def get_recent_prompts(user_name: str):
    prompts = redis.get_list(user_name)
    response = []
    for prompt in prompts[::-1]:
        prompt = json.loads(prompt)
        response.append(prompt)

    return {"user_prompts": response}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    try:
        while True:
            try:
                data = await websocket.receive_json()
                user_prompt = data['prompt']
                tool = data['tool']
                print(f"Received from client: {data}")
                
                response_generator = send_response(user_prompt, ToolEnum(tool))
                
                response = ""
                try:
                    async for chunk in response_generator:
                        if chunk:  # Only process non-empty chunks
                            response += chunk
                            await websocket.send_json({"chunk": chunk, "status": "inprogress"})
                            await asyncio.sleep(0.001)
                    
                    print('Full response:')
                    print(response)
                except Exception as e:
                    print(f"Error processing chunks: {e}")
                    await websocket.send_json({"chunk": f"Error: {str(e)}", "status": "error"})
                finally:
                    # Send an end-of-stream marker if needed
                    await websocket.send_json({"status": "complete"})
                    pass

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
                    "tool": tool,
                    "response": response
                }
                db.insert("prompt_log", data)
                data['timestamp'] = data['timestamp'].isoformat()
                redis.push("user", json.dumps(data))
                redis.trim("user", 0, 9)
                print(redis.get_list("user"))
                
            except asyncio.CancelledError:
                raise
                
            except Exception as e:
                print(f"Error in websocket: {e}")
                await websocket.send_json({"error": str(e)})
                continue
                
    except asyncio.CancelledError:
        print("Client disconnected")
        
    except Exception as e:
        print(f"WebSocket connection error: {e}")
        
    finally:
        try:
            await websocket.close()
        except:
            pass
