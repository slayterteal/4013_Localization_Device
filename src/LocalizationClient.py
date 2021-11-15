#!/usr/bin/env python3

import asyncio
import websockets
import serial

SERVER_IP = "ws://10.8.62.90:8000"
SERIAL_PORT = serial.Serial('COM5', 9600, timeout=1)

async def poll_for_localization_data(websocket):
    while True:
        greeting = await websocket.recv()
        print(f"<<< Returned Data {greeting}")

async def connect():
    async with websockets.connect(SERVER_IP) as websocket:
        await poll_for_localization_data(websocket)

async def pollSerial():
    while True:
        data = SERIAL_PORT.readline()
        if len(data) >= 1:
            print(data.decode("utf-8"))

async def run():
    event_loop = asyncio.get_event_loop()
    event_loop.create_task(connect())
    event_loop.create_tast(pollSerial())
    event_loop.run_forever()

# asyncio.run(run())

asyncio.run(connect())

