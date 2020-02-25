#!/usr/bin/env python
#------------------------------------------------------
#
#       This is a program for JoystickPS2 Module.
#
#       This program depend on PCF8591 ADC chip. Follow 
#   the instruction book to connect the module and 
#   ADC0832 to your Raspberry Pi.
#
#------------------------------------------------------
import sys
import os
sys.path.append(os.path.abspath("/home/pi/s2gpio-master/s2gpio"))
import joystick_PS2_python3 as joystick
import time

direction = joystick.read()
tmp = str(direction)
print (tmp)

