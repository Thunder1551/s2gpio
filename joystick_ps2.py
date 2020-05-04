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

def read_PCF8591(channel, y_pin, x_pin, bt_pin):
    ADC.setup(channel)                 # Setup PCF8591
    status = ''
    state = ['home', 'pressed', 'down_left', 'down_right', 'up_left', 'up_right', 'down', 'up', 'left', 'right']
    i = 0
    if ADC.read(bt_pin) <= 5:
        i = 1       #Button pressed
    elif ADC.read(y_pin) <= 5 and ADC.read(x_pin) <= 5:
        i = 2       #down_left      
    elif ADC.read(y_pin) <= 5 and ADC.read(x_pin) >= 250:
        i = 3       #down_right
    elif ADC.read(y_pin) >= 250 and ADC.read(x_pin) <= 5:
        i = 4       #up_left      
    elif ADC.read(y_pin) >= 250 and ADC.read(x_pin) >= 250:
        i = 5       #up_right
    elif ADC.read(y_pin) <= 5:
        i = 6       #down
    elif ADC.read(y_pin) >= 250:
        i = 7       #up
    elif ADC.read(x_pin) <= 5:
        i = 8       #left
    elif ADC.read(x_pin) >= 250:
        i = 9       #right
    if state[i] != None and state[i] != status:
        return state[i]
    
def read_MCP3008(spiPort, spiDevice, y_pin, x_pin, bt_pin):
    mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(spiPort, spiDevice))
    status = ''
    state = ['home', 'pressed', 'down_left', 'down_right', 'up_left', 'up_right', 'down', 'up', 'left', 'right']
    i = 0
    if mcp.read_adc(bt_pin) <= 5:
        i = 1       #Button pressed
    elif mcp.read_adc(y_pin) <= 5 and mcp.read_adc(x_pin) <= 5:
        i = 2       #down_left      
    elif mcp.read_adc(y_pin) <= 5 and mcp.read_adc(x_pin) >= 1000:
        i = 3       #down_right
    elif mcp.read_adc(y_pin) >= 1000 and mcp.read_adc(x_pin) <= 5:
        i = 4       #up_left      
    elif mcp.read_adc(y_pin) >= 1000 and mcp.read_adc(x_pin) >= 1000:
        i = 5       #up_right
    elif mcp.read_adc(y_pin) <= 5:
        i = 6       #down
    elif mcp.read_adc(y_pin) >= 1000:
        i = 7       #up
    elif mcp.read_adc(x_pin) <= 5:
        i = 8       #left
    elif mcp.read_adc(x_pin) >= 1000:
        i = 9       #right
    if state[i] != None and state[i] != status:
        return state[i]
