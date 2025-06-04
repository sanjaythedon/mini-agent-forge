import asyncio
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

    try:
        while True:
            try:
                # Wait for a message from the client
                data = await websocket.receive_json()
                print(f"Received from client: {data}")
                
                # Get the async generator from send_response
                response_generator = send_response(data['prompt'], ToolEnum(data['tool']))
                
                # Process each chunk as it comes asynchronously
                async for chunk in response_generator:
                    # Send each chunk immediately to the client
                    await websocket.send_text(chunk)
                    
                    # Small delay to prevent overwhelming the client
                    await asyncio.sleep(0.001)
                
                # Send an end-of-stream marker
                await websocket.send_json({"status": "complete"})
                
            except asyncio.CancelledError:
                # Handle client disconnection
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
