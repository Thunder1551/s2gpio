#!/usr/bin/env python
import PCF8591 as ADC
import RPi.GPIO as GPIO
import time
import math
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

def read_pcf8591(channel,analogInput):
    ADC.setup(channel)
    temp = 0;
    for x in range (5):
        try:
            analogVal = ADC.read(analogInput)
            Vr = 5 * float(analogVal) / 255
            Rt = 10000 * Vr / (5 - Vr)
            temp = 1/(((math.log(Rt / 10000)) / 3950) + (1 / (273.15+25)))
            temp = temp - 273.15
        except ValueError:
            print("math domain error")
        if (temp != 0 and temp != 255):
           return temp

# still calculating wrong value
def read_mcp3008(spiPort, spiDevice, analogInput):
    mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(spiPort, spiDevice))
    temp = 0;
    for x in range (5):
        try:
            analogVal = mcp.read_adc(analogInput)
            Vr = 5 * float(analogVal) / 1023
            Rt = 10000 * Vr / (5 - Vr)
            temp = 1/(((math.log(Rt / 10000)) / 3950) + (1 / (273.15+25)))
            temp = temp - 273.15
        except ValueError:
            print("math domain error")
        if (temp != 0 and temp != 1023):
           return temp

if __name__ == '__main__':
    # For testing the sensor at default channel i2C 0x48 and input pin AIN2
    pcfValue = read_pcf8591(0x48,2);
    print(pcfValue)
    # For testin the sensor at SPI port 0, device 0, AIN0
    mcpValue = read_mcp3008(0,0,0);
    print(mcpValue) 


