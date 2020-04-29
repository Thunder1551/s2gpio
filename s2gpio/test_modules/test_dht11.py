import sys
import os
sys.path.append(os.path.abspath("/home/pi/s2gpio-master/s2gpio/modules"))
import dht11
import time

temp, hum = dht11.read(17)
print(temp, hum)
