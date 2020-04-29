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
import PCF8591 as ADC
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import time

def setup():
    ADC.setup(0x48)                 # Setup PCF8591
    global state

def direction():    #get joystick result
    state = ['home', 'up', 'down', 'left', 'right', 'pressed']
    i = 0
    #print(ADC.read(0))
    #print(ADC.read(1))
    if ADC.read() <= 5:
        i = 1       #up       
    if ADC.read(4) >= 250:
        i = 2       #down
    if ADC.read(3) >= 250:
        i = 3       #left
    if ADC.read(3) <= 5:
        i = 4       #right
    if ADC.read(2) == 0:
        i = 5       # Button pressed

    if ADC.read(y_pin) - 125 < 15 and ADC.read(y_pin) - 125 > -15   and ADC.read(x_pin) - 125 < 15 and ADC.read(x_pin) - 125 > -15 and ADC.read(bt_pin) == 255:
        i = 0
    
    return state[i]

def loop():
    status = ''
    while True:
        tmp = direction()
        if tmp != None and tmp != status:
            print (tmp)
            status = tmp

def destroy():
    pass
"""
if __name__ == '__main__':      # Program start from here
    setup()
    try:
        loop()
    except KeyboardInterrupt:   # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        destroy()
"""


def read_PCF8591(channel, y_pin, x_pin, bt_pin):
    ADC.setup(channel)                 # Setup PCF8591
    status = ''
    state = ['home', 'down', 'up', 'right', 'left', 'pressed']
    i = 0
    #print(ADC.read(0))
    #print(ADC.read(1))
    if ADC.read(y_pin) <= 5:
        i = 1       #down       
    if ADC.read(y_pin) >= 250:
        i = 2       #up
    if ADC.read(x_pin) >= 250:
        i = 3       #right
    if ADC.read(x_pin) <= 5:
        i = 4       #left
    if ADC.read(bt_pin) <= 5:
        i = 5       #Button pressed

    if ADC.read(y_pin) - 125 < 15 and ADC.read(y_pin) - 125 > -15   and ADC.read(x_pin) - 125 < 15 and ADC.read(x_pin) - 125 > -15 and ADC.read(bt_pin) == 255:
        i = 0
    if state[i] != None and state[i] != status:
        return state[i]
    
def read_mcp3008(spiPort, spiDevice, y_pin, x_pin, bt_pin):
    mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(spiPort, spiDevice))
    status = ''
    state = ['home', 'down', 'up', 'right', 'left', 'pressed']
    i = 0
    #print(ADC.read(0))
    #print(ADC.read(1))
    if mcp.read_adc(y_pin) <= 5:
        i = 1       #down       
    if mcp.read_adc(y_pin) >= 1000:
        i = 2       #up
    if mcp.read_adc(x_pin) >= 1000:
        i = 3       #right
    if mcp.read_adc(x_pin) <= 5:
        i = 4       #left
    if mcp.read_adc(bt_pin) <= 5:
        i = 5       #Button pressed

    if ADC.read(y_pin) - 125 < 15 and ADC.read(y_pin) - 125 > -15   and ADC.read(x_pin) - 125 < 15 and ADC.read(x_pin) - 125 > -15 and ADC.read(bt_pin) == 255:
        i = 0
    if state[i] != None and state[i] != status:
        return state[i]