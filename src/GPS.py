import serial #pip install pyserial
import time

mport = "/dev/serial0" #magic serial location of stuff

def parseGPS(data):
    if data[0:6] == "$GPGGA": #other NMEA headers have info, but this header contains all the stuff we want
        s = data.split(",")
        if s[7] == '0' or s[7]=='00':
            print ("no satellite data available: ", s[1])
            return
        #print("satellite(s): ", s[7])

        #uncomment if we dont want time in seconds only
        #time = s[1][0:2] + ":" + s[1][2:4] + ":" + s[1][4:6]
        #s[1] = time
        
        #print(s)

        return data

ser = serial.Serial(mport,9600,timeout = 2)

def getGPSData():
        try:
                
                dat = ser.readline().decode()
                return parseGPS(dat)
        except KeyboardInterrupt:
                print("Exiting")
                exit()
        except Exception as e:
                print("Error: ", e)
                pass
         
if __name__ == "__main__":
        while True:
                getGPSData()
