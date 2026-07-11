import asyncio
import websockets


async def listen():

    async with websockets.connect("ws://127.0.0.1:8000/ws") as websocket:

        print("Connected")

        while True:

            message = await websocket.recv()

            print(message)


asyncio.run(listen())