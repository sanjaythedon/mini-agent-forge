import json
from fastapi import FastAPI, WebSocket
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from Redis import Redis
import os
from dotenv import load_dotenv
from ws_manager import WebSocketManager
load_dotenv()

redis = Redis(
    host=os.getenv("REDIS_HOST"),
    port=os.getenv("REDIS_PORT"),
    db=os.getenv("REDIS_DB")
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
    try:
        prompts = redis.get_list(user_name)
        response = []
        for prompt in prompts[::-1]:
            prompt = json.loads(prompt)
            response.append(prompt)

        return {"user_prompts": response}
    except Exception as e:
        print(f"Error getting chat history: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for handling real-time communication with clients.
    
    This endpoint manages the WebSocket connection, processes incoming messages,
    generates responses using LLM, and handles database operations through the WebSocketManager.
    """
    websocket_manager = WebSocketManager(websocket)
    await websocket_manager.handle_connection()
