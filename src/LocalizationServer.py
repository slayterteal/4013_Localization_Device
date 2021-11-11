#!/usr/bin/env python3

# WS server example

import asyncio
import websockets
import glob
import threading
from GPS import getGPSData

STORAGE_LOCATION = glob.glob("/media/pi/*")

def __async__server(): # server entrypoint
    asyncio.run(handle_connection())

async def send(websocket, path):
    while True:
        try:
            result = await websocket.send("data")
        except websockets.ConnectionClosed:
            print("Client has disconnected")
            break

        print(f">>> Data Sent: {result}")

async def handle_connection():
    print("handle_connection is being called...")
    async with websockets.serve(send, "localhost", 8000): # On connection, constantly send data to client.
        print("waiting for connections...")
        await asyncio.Future()

def __async__data_write(): # usb/sd entrypoint
    asyncio.run(handle_data())

async def handle_data():
    # TODO: Grab data from IMU/GPU (likely from a wrapper function). 
    #       Each communication process should attempt to recieve the data from the IMU/GPS
    # TODO: send data through USB!
    # event_loop = asyncio.get_event_loop()
    # event_loop.create_task(store_to_sd())
    # event_loop.run_forever()
    await store_to_sd()
    
async def store_to_sd():
    data = "WOWZA!"
    print(data)
    while True:
        await write_to_sd(data)

async def write_to_sd(data):
    if(len(STORAGE_LOCATION) == 0):
        return False
    else:
        PATH = STORAGE_LOCATION[0]+"/data.txt" #TODO: Change to CSV file extension
        f = open(PATH, "a")
        f.write(str(data + "\n")) #TODO: Might get rid of the /n for testing
        f.close()
        return True


async_thread = threading.Thread(target=__async__data_write)
server_thread = threading.Thread(target=__async__server)

async_thread.start()
server_thread.start()
print("Threads are running.")

diff --git a/src/LocalizationClient.py b/src/LocalizationClient.py
