#!/usr/bin/env python3

import asyncio
import websockets
import serial
import threading

SERVER_IP = "ws://localhost:6969"
SERIAL_PORT = serial.Serial('COM5', 9600, timeout=1)

async def poll_for_localization_data(websocket):
    while True:
        dataFromServer = await websocket.recv()
        print(f"<<< Returned Data {dataFromServer}")

async def connect():
    async with websockets.connect(SERVER_IP) as websocket:
        await poll_for_localization_data(websocket)

def handle_server():
    asyncio.run(connect())

def pollSerial():
    while True:
        data = SERIAL_PORT.readline()
        if len(data) >= 1:
            str_data = data.decode("utf-8")
            print(f'Serial Data: {str_data}')

wireless = threading.Thread(target=handle_server)
serial_comm = threading.Thread(target=pollSerial)

wireless.start()
serial_comm.start()



