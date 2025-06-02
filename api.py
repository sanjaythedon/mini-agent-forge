from fastapi import FastAPI
from main import send_response

from models import Payload

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.post("/run")
def run(payload: Payload):
    response = send_response(payload.prompt, payload.tool)
    return {"message": response}

