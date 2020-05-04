import sys
import os
sys.path.append(os.path.abspath("/home/pi/s2gpio-master/s2gpio/modules"))
import bmp

try:
    pressure, altitude = bmp.read_sensor()
    print(pressure, altitude)
except OSError:
    print("not connected")
