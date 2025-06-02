from fastapi import FastAPI

from models import Payload

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/run")
def run(payload: Payload):
    return {"Hello": "World"}

