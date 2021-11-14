#will need to do serial magic that I dont understand...
import serial #pip install pyserial
import time

mport = "/dev/ttyAMA0" #magic serial place gpio14 goes to

def parseGPS(data):
    if data[0:6] == "$GPGGA":
        s = data.split(",")
        if s[7] == '0' or s[7]=='00':
            print ("no satellite data available")
            return
        lat = s[2]
        lon = s[4]
        print("satellite(s): ", s[7])

        time = s[1][0:2] + ":" + s[1][2:4] + ":" + s[1][4:6]
        print(time)

        return  str(s)

def decode(coord):
    l = list(coord)
    for i in range(0,len(l)-1):
            if l[i] == "." :
                    break
    base = l[0:i-2]
    degi = l[i-2:i]
    degd = l[i+1:]
    #print(base,"   ",degi,"   ",degd)
    baseint = int("".join(base))
    degiint = int("".join(degi))
    degdint = float("".join(degd))
    degdint = degdint / (10**len(degd))
    degs = degiint + degdint
    full = float(baseint) + (degs/60)
    #print(full)
    
    return full

ser = serial.Serial(mport,9600,timeout = 2)

while True:
    # try:
    dat = ser.readline().decode()
    if len(dat) == 0:
        data = "Nothing"
    else:
        data = "parseGPS()"
        data = parseGPS(dat)
        # print(mylat , "N " , mylon, "W")
    print(data)
    # except:
        #pass
        # print("error")
        # exit()
