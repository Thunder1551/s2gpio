import sys
import os
sys.path.append(os.path.abspath("/home/pi/s2gpio-master/s2gpio/modules"))
import lcd1602_i2c

try:
    message = 'Hello World'
    lcd1602_i2c.write_message(str(message), 1)
except OSError:
    print("not connected")