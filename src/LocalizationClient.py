#!/usr/bin/env python3

# WS client example

import asyncio
import websockets

server_ip = "ws://localhost:8000"

async def poll_for_localization_data(websocket):
    while True:
        greeting = await websocket.recv()
        print(f"<<< Returned Data {greeting}")

async def run():
    async with websockets.connect(server_ip) as websocket:
        await poll_for_localization_data(websocket)

asyncio.run(run())


