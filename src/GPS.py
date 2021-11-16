import serial 

port = "/dev/serial0" 
ser = serial.Serial(port,9600,timeout = 2)

def parseGPS(data):
    if data[0:6] == "$GPGSV": # other NMEA headers have info, but this header contains all the stuff we want
        s = data.split(",")
        # if s[7] == '0' or s[7]=='00':
        #     # print(str(s)) # For print RAW for debugging
        #     return "No satellite data available."
        return data
    else:
        return "No satellite data available."

def getGPSData():
        try: 
                dat = ser.readline().decode()
                # print(f'unparsed data: {dat}')
                print(parseGPS(dat))
                # return parseGPS(dat)
        except KeyboardInterrupt:
                print("\nExiting")
                exit()
        except Exception as e:
                print("Error: ", e)
                pass
         
if __name__ == "__main__":
        while True:
                getGPSData()
