#!/usr/bin/env python3

import websockets
import asyncio
import glob
import threading
import serial
from os.path import exists
from imu import getIMUData
from GPS import getGPSData

STORAGE_LOCATIONS = glob.glob("/media/pi/*")
DATA_PARAMS = "X Gyro,Y Gyro,Z Gyro,X Accel,Y Accel,Z Accel,X Mag,Y Mag,Z Mag,NMEA code for Global Positioning System Fix Data,time,latitude,N,Latitude,W,GPS fix,satellite count,Horizontal dilution of position,Altitide,,Height of geoid,,,check sum \n"

def __async__server(): # server entrypoint
    asyncio.run(handle_connection())

async def send(websocket, path):
    while True:
        try:
            localization_data = await getData()
            message = DATA_PARAMS + localization_data + "\n"
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
    while True:
        localization_data = await getData()
        await write_to_sd(localization_data)
        await sendSerial(localization_data)

async def getData():
    try:
        gps_data = getGPSData()
        imu_data = getIMUData()
        return imu_data + str(gps_data)
    except:
        return "partial calculation error"

async def sendSerial(message):
    port = serial.Serial('/dev/ttyAMA1', 9600) # TODO: make sure this doesn't need to be changed!!
    byte_header = bytes(DATA_PARAMS, 'utf-8')
    byte_message = bytes(message, 'utf-8')
    port.write(byte_header)
    port.write(byte_message)
    port.close()

async def write_to_sd(data):
    if(len(STORAGE_LOCATIONS) == 0):
        return False
    else:
        PATH = STORAGE_LOCATIONS[0]+"/LocalizationData.csv"
        if(exists(PATH)):
            f = open(PATH, "a")
            f.write(str(data + "\n"))
            f.close()
        else:
            f = open(PATH, "w")
            f.write(DATA_PARAMS)
            f.write(str(data + "\n"))
            f.close()
        return True


async_thread = threading.Thread(target=__async__data_write)
server_thread = threading.Thread(target=__async__server)

async_thread.start()
server_thread.start()
print("Threads are running.")

