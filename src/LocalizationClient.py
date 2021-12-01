#!/usr/bin/env python3

import asyncio
import websockets
import serial
import threading

SERVER_IP = "ws://localhost:6969"

async def poll_for_localization_data(websocket):
    while True:
        try:
            dataFromServer = await websocket.recv()
            print(f"<<< Returned Data {dataFromServer}")
        except:
            # print("No DATA sent...")
            return

async def connect():
    while True:
        try:
            async with websockets.connect(SERVER_IP) as websocket:
                await poll_for_localization_data(websocket)
        except:
            # print("no server found")
            pass

def handle_server():
    asyncio.run(connect())

def pollSerial():
    while True:
        try:
            SERIAL_PORT = serial.Serial('COM5', 9600, timeout=1)
        except:
            # print("No serial port found")
            pass
        else:
            data = SERIAL_PORT.readline()
            if len(data) >= 1:
                str_data = data.decode("utf-8")
                print(f'Serial Data: {str_data}')

wireless = threading.Thread(target=handle_server)
serial_comm = threading.Thread(target=pollSerial)

serial_comm.start()
wireless.start()




