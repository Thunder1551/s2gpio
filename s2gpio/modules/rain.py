#/usr/bin/env python
import RPi.GPIO as GPIO
import PCF8591 as ADC
import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

# Method that is called by s2gpio to get the rain probability using PCF8591 module
# returns a relative perventage value between 0 (no rain) and 1 (rain)
def read_PCF8591(channel,analogInput):
    ADC.setup(channel)
    value = 0;
    runs = 5;
    # read sensor a few times to ensure a good value
    for x in range(runs):
        analogVal = ADC.read(analogInput)
        value += analogVal;
    # calculate the average of the sensing runs
    avgValue = value / runs;
    percentage = 1 - (avgValue / 255)
    return round(percentage,2);

# Method that is called by s2gpio to get the rain probability using MCP3008 module
# returns a relative perventage value between 0 (no rain) and 1 (rain)
def read_MCP3008(spiPort, spiDevice, analogInput):
    mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(spiPort, spiDevice))
    value = 0;
    runs = 5;
    # read sensor a few times to ensure a good value
    for x in range(runs):
        analogVal = mcp.read_adc(analogInput)
        value += analogVal;
    # calculate the average of the sensing runs
    avgValue = value / runs;
    percentage = 1 - (avgValue / 1023)
    return round(percentage,2);           

if __name__ == '__main__':
    # Test the sensor at default channel 0x48 and input pin AIN3
    pcfValue = read_PCF8591(0x48,3);
    print(pcfValue)
    # Test the sensor at SPI port 0, device 0, AIN4
    mcpValue = read_MCP3008(0,0,4);
    print(mcpValue)