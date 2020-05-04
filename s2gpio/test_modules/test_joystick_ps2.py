#!/usr/bin/env python
import sys
import os
sys.path.append(os.path.abspath("/home/pi/s2gpio-master_2904-broken/s2gpio/modules"))
import joystick_ps2

# To test your sensor uncomment the lines of code that are not relevant.
# If you are using a PCF8591 on default channel 0x48 and analog Input AIN3. Otherwise change parameters.
try:
    pcf_value = joystick_ps2.read_PCF8591(0x48,3,2,1)
    print (pcf_value)
except OSError:
    print("Not connected or wrong channel")
# If you are using a MCP3008 on device 0, port 0 and analog Inputs y_pin = AIN7, x_pin = AI6 and bt_pin = AI5.
# Otherwise adjust parameters.
mcp_value = joystick_ps2.read_MCP3008(1,0,7,6,5)
print (mcp_value)
