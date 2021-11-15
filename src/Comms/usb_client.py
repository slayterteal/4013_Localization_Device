import serial
serialPort = serial.Serial('COM5', 9600, timeout=1)

while True:

    #read data from serial port
    data = serialPort.readline()

    #if there is smth do smth
    if len(data) >= 1:
        print(data.decode("utf-8"))

