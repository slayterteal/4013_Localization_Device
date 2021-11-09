import serial

port = serial.Serial('/dev/ttyAMA0', 9600)
print(port)
# send the data
port.write(b'0123456')
port.close() 