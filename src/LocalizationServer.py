#!/usr/bin/env python3

import websockets
import asyncio
import glob
import threading
import serial
# from imu import getIMUData

STORAGE_LOCATIONS = glob.glob("/media/pi/*")

def __async__server(): # server entrypoint
    asyncio.run(handle_connection())

async def send(websocket, path):
    while True:
        try:
            localization_data = await getData()
            result = await websocket.send(localization_data)
            print(f">>> Data Sent")
        except websockets.ConnectionClosed:
            print("Client has disconnected")
            break

async def handle_connection():
    print("handle_connection is being called...")
    async with websockets.serve(send, "localhost", 6969): 
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
    while True:
        localization_data = "getData() "
        await store_to_sd(localization_data)
        await sendSerial(localization_data)

async def getData():
    # gps_data = getGPSData()
    imu_data = "getIMUData()"
    return imu_data

async def sendSerial(message):
    #port = serial.Serial('/dev/serial1', 9600) # TODO: make sure this doesn't need to be changed!!
    #byte_message = bytes(message, 'utf-8')
    #port.write(byte_message)
    #port.close()
    print("Sent Data via Serial")
    
async def store_to_sd(data):
    await write_to_sd(data)

async def write_to_sd(data):
    if(len(STORAGE_LOCATIONS) == 0):
        return False
    else:
        PATH = STORAGE_LOCATIONS[0]+"/LocalizationData.csv" #TODO: Change to CSV file extension
        f = open(PATH, "w")
        f.write(str(data + "\n")) #TODO: Might get rid of the /n for testing
        f.close()
        return True


async_thread = threading.Thread(target=__async__data_write)
server_thread = threading.Thread(target=__async__server)

async_thread.start()
# server_thread.start()
print("Threads are running.")

