from typing import Union

from fastapi import FastAPI, WebSocket
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
def read_root():
    return {"Wowwee": "Zowee"}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)