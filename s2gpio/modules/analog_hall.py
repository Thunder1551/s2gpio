#/usr/bin/env python
import RPi.GPIO as GPIO
import PCF8591 as ADC
import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

# 
def read_PCF8591(channel,analogInput):
    ADC.setup(channel)
    value = 0;
    runs = 5;
    # read sensor a few times to ensure a good value
    for x in range(runs):
        analogVal = ADC.read(analogInput)
        value += analogVal;
        time.sleep(0.1);
    # calculate the average of the sensing runs
    avgValue = value / runs;
    percentage = avgValue / 255
    return round(percentage,2);


def read_MCP3008(spiPort, spiDevice, analogInput):
    mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(spiPort, spiDevice))
    value = 0;
    runs = 5;
    # read sensor a few times to ensure a good value
    for x in range(runs):
        analogVal = mcp.read_adc(analogInput)
        value += analogVal;
        time.sleep(0.1);
    # calculate the average of the sensing runs
    avgValue = value / runs;
    percentage = avgValue / 1023
    return round(percentage,2);           

if __name__ == '__main__':
    # For testing the sensor at default channel i2C 0x48 and input pin AIN3
    pcfValue = read_PCF8591(0x48,3);
    print(pcfValue)
    # For testin the sensor at SPI port 0, device 0, AIN4
    mcpValue = read_MCP3008(0,0,4);
    print(mcpValue)
    

