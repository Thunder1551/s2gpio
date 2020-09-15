# s2gpio 
![](https://github.com/thunder1551/s2gpio/blob/master/docs/images/RoboRasp.png) 
## A Scratch 2 Extensions For The Raspberry Pi To Read Analog Sensor Values Within Scratch

The Extension is based on Alan Yorick's Scratch 2 Extenion # s2-pi incl. WebSocket communication and was developed according to [his tutorial](https://mryslab.github.io/s2-pi/)
If you are interested in making your own Extension please refer to the [ScratchX tutorial](https://github.com/LLK/scratchx) and the [s2-pi tutorial](https://mryslab.github.io/s2-pi/) first.

The aim of this Extension is to have an Scratch interal solution for reading analog sensors to use them in Scratch programms.
# Note: Refering to the ScratchX documentation this is NOT an official nor an supported Scratch 2 Extension.
# Use at your own risk!

It is version 1.0 and may not be the last version
Nevertheless, the goal of the development was a functioning extension for reading out analog sensors with the Raspberry Pi.
The extension is intended to encourage other developers to create their own extensions based on Alan Yorik's WebSocket Communication and this idea to realize the sensing in Python.

To install type:
`
sudo pip3 install s2gpio
`

The Extension cointains block-functionalities to read analog sensors via ADCs MCP3008 and PCF8591.
Supported analog sensors are:
- hall switch
- flame
- gas
- photoresistor
- rain
- sound
- thermistor
- ps2-joystick

Furthermore the I2C interface can be used to read a BMP085/180 sensor oder display messages on a LCD1602-Display.


