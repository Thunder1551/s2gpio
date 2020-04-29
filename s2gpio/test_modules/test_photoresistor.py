import sys
import os
sys.path.append(os.path.abspath("/home/pi/s2gpio-master/s2gpio/modules"))
import photoresistor

# To test your sensor uncomment the lines of code that are not relevant.
# If you are using a PCF8591 on default channel 0x48 and analog Input AIN1. Otherwise change parameters.
pcf_value = photoresistor.read_pcf8591(0x48,1);
print(pcf_value)
# If you are using a MCP3008 on device 0, port 0 and analog Input AIN2. Otherwise change parameters.
mcp_value = photoresistor.read_mcp3008(0,0,2);
print(mcp_value)
