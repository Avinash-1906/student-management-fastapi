from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from websocket_manager import manager

websocket_router = APIRouter()

@websocket_router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):

    await manager.connect(websocket)

    print("Client Connected")

    try:
        while True:
            await websocket.receive_text()

    except WebSocketDisconnect:

        manager.disconnect(websocket)

        print("Client Disconnected")