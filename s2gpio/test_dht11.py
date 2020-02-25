import json
import os
import sys
import time
import datetime
from subprocess import call

import sys
import os
sys.path.append(os.path.abspath("/home/pi/s2gpio-master/s2gpio"))
import dht11_pigpio
import bmp_read
import joystick_PS2_python3
import i2c_lcd1602_write

temp, hum = dht11_pigpio.read(17)
print(temp, hum)
ts = int(time.time()*1000)
ts2 = str(ts)
print(ts2)
print(ts)