from fastapi import FastAPI
from main import send_response
from fastapi.websockets import WebSocket
from models import Payload, ToolEnum

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.post("/run")
def run(payload: Payload):
    response = send_response(payload.prompt, payload.tool)
    return {"message": response}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    while True:
        data = await websocket.receive_json()
        print(f"Received from client: {data}")
        for response in send_response(data['prompt'], ToolEnum(data['tool'])):
            await websocket.send_text(response)
    

