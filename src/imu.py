# Main IMU data collection file with CSV file writing support
import time
import board
from adafruit_bno055 import BNO055_I2C as bno055
import csv

i2c = board.I2C()
sensor = bno055(i2c)

def getIMUData():

    fields = "X Gyro,Y Gyro,Z Gyro,X Accel,Y Accel,Z Accel,X Mag,Y Mag,Z Mag\n"
        
    # Sensor data rows for Gyro, Linear Acceleration, and Magnetic Field
    gyro = list(sensor.gyro)
    lin_acc = list(sensor.linear_acceleration)
    mag = list(sensor.magnetic)
            
    # Rounds to the third decimal place
    gyroString = ""
    lin_accString = ""
    magString = ""
    for i in range(0, 3):
        gyro[i] = round(gyro[i], 3)
        lin_acc[i] = round(lin_acc[i], 3)
        mag[i] = round(mag[i], 3)
        
        gyroString += str(gyro[i]) + ","
        lin_accString += str(lin_acc[i]) + ","
        
        if i is not 2:
            magString += str(mag[i]) + ","
        else:
            magString += str(mag[i])
    
    final = fields + gyroString + lin_accString + magString + "\n"
    return final
    
for i in range(20):
    print(getIMUData())
