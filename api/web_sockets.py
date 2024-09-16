import threading
import uvicorn
import asyncio
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from python_event_bus import EventBus

ws_app = FastAPI()

ws_app.mount('/static', StaticFiles(directory='api/static', html=True), name='static')

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        EventBus.call("new_cli")

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str, ws: WebSocket=None):
        for connection in self.active_connections:
            if (ws!=connection):
                await connection.send_text(message)


manager = ConnectionManager()

@ws_app.get("/")
def read_root():
    EventBus.call("connect", "WebSocket API conected.")
    return {"content": "Hello World"}

@ws_app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Client #{client_id} says: {data}", websocket)
            EventBus.call("ws_message", f"Client #{client_id} says: {data}")
            EventBus.call("message", f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat", websocket)
        EventBus.call("ws_message", f"Client #{client_id} left the chat")
        EventBus.call("message", f"Client #{client_id} left the chat")


@EventBus.on("qt5_message")
def qt5_message(message):
    loop = asyncio.new_event_loop()
    threading.Thread(target=run_coroutine, args=(loop, message)).start()

def run_coroutine(loop, message):
    asyncio.set_event_loop(loop)
    loop.run_until_complete(manager.broadcast(f"QT5. {message}"))
    

def run():
    config = uvicorn.Config(ws_app, host="127.0.0.1", port=8000, log_level="info")
    server = uvicorn.Server(config)
    server.run()