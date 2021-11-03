#!/usr/bin/env python3

import glob 

STORAGE_LOCATION = glob.glob("/media/pi/*")

class store_sd:
    def write(self, data):
        if(len(STORAGE_LOCATION) == 0):
            return False
        else:
            PATH = STORAGE_LOCATION[0]+"/data.txt"
            f = open(PATH, "w")
            f.write(str(data))
            f.close()
            return True
