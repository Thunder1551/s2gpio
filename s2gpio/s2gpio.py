#!/usr/bin/env python3

"""
s2gpio.py

 Copyright (c) 2016-2018 Alan Yorinks All right reserved.

 Python Banyan is free software; you can redistribute it and/or
 modify it under the terms of the GNU AFFERO GENERAL PUBLIC LICENSE
 Version 3 as published by the Free Software Foundation; either
 or (at your option) any later version.
 This library is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 General Public License for more details.

 You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
 along with this library; if not, write to the Free Software
 Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

"""
import json
import os
import sys
import time
import datetime
from subprocess import call

import sys
import os
sys.path.append(os.path.abspath("/home/pi/s2gpio-master/s2gpio/modules"))
import analog_hall
import bmp_read
import dht11
import flame
import joystick_ps2
import lcd1602_i2c
import photoresistor
import rain
import sound
import thermistor


import pigpio
import psutil
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket


# This class inherits from WebSocket.
# It receives messages from the Scratch and reports back for any digital input
# changes.
class S2Gpio(WebSocket):

    def handleMessage(self):
        # get command from Scratch2
        payload = json.loads(self.data)
        print(payload)
        client_cmd = payload['command']
        # When the user wishes to set a pin as a digital Input
        if client_cmd == 'input':
            pin = int(payload['pin'])
            self.pi.set_glitch_filter(pin, 20000)
            self.pi.set_mode(pin, pigpio.INPUT)
            self.pi.callback(pin, pigpio.EITHER_EDGE, self.input_callback)
        # when a user wishes to set the state of a digital output pin
        elif client_cmd == 'digital_write':
            pin = int(payload['pin'])
            self.pi.set_mode(pin, pigpio.OUTPUT)
            state = payload['state']
            if state == '0':
                self.pi.write(pin, 0)
            else:
                self.pi.write(pin, 1)
        elif client_cmd == 'digital_write2':
            pin = int(payload['pin'])
            self.pi.set_mode(pin, pigpio.OUTPUT)
            state = payload['state']
            #self.pi.write(pin, 1)
            #self.pi.set_glitch_filter(pin, 20000)
            #self.pi.set_mode(pin, pigpio.INPUT)
            #self.pi.callback(pin, pigpio.EITHER_EDGE, self.input_callback2)
            number = 5
            payload = {'report': 'digital_input_change3', 'pin': str(pin), 'level': str(number)}
            msg = json.dumps(payload)
            self.sendMessage(msg)
            if state == '0':
                self.pi.write(pin, 0)
            else:
                self.pi.write(pin, 1)
        # catching write block and returning pin number to js
        elif client_cmd == 'write':
            pin = int(payload['pin'])
            #self.pi.set_mode(pin, pigpio.OUTPUT)
            state = payload['state']
            #self.pi.write(pin, 1)
            #self.pi.set_glitch_filter(pin, 20000)
            #self.pi.set_mode(pin, pigpio.INPUT)
            #self.pi.callback(pin, pigpio.EITHER_EDGE, self.input_callback2)
            #number = 5
            tempvar, humvar = dht11_pigpio.read(pin)
            #payload = {'report': 'write_return', 'pin': str(pin), 'level': str(number)}
            payload = {'report': 'write_return', 'pin': str(tempvar), 'level': str(humvar)}
            msg = json.dumps(payload)
            self.sendMessage(msg)
            if state == '0':
                self.pi.write(pin, 0)
            else:
                self.pi.write(pin, 1)
        # when a user wishes to set a pwm level for a digital input pin
        elif client_cmd == 'analog_write':
            pin = int(payload['pin'])
            self.pi.set_mode(pin, pigpio.OUTPUT)
            value = int(payload['value'])
            self.pi.set_PWM_dutycycle(pin, value)

        elif client_cmd == 'servo':
            # HackEduca ---> When a user wishes to set a servo:
            # Using SG90 servo:
            # 180° = 2500 Pulses; 0° = 690 Pulses
            # Want Servo 0°-->180° instead of 180°-->0°:
            # Invert pulse_max to pulse_min
            # pulse_width = int((((pulse_max - pulse_min)/(degree_max - degree_min)) * value) + pulse_min)
            # Where:
            # Test the following python code to know your Pulse Range: Replace it in the formula
            # >>>>----------------------->
            # import RPi.GPIO as GPIO
            # import pigpio
            # Pulse = 690 # 0°
            # Pulse = 2500 # 180°
            # pi = pigpio.pi()
            # pi.set_mode(23, pigpio.OUTPUT)
            # pi.set_servo_pulse_width(23, Pulse)
            # pi.stop()
            # <------------------------<<<<<
            pin = int(payload['pin'])
            self.pi.set_mode(pin, pigpio.OUTPUT)
            value = int(payload['value'])
            DegreeMin = 0
            DegreeMax = 180
            PulseMin = 2500
            PulseMax = 690
            Pulsewidth = int((((PulseMax - PulseMin) / (DegreeMax - DegreeMin)) * value) + PulseMin)
            self.pi.set_servo_pulsewidth(pin, Pulsewidth)
            time.sleep(0.01)

        # when a user wishes to output a tone
        elif client_cmd == 'tone':
            pin = int(payload['pin'])
            self.pi.set_mode(pin, pigpio.OUTPUT)

            frequency = int(payload['frequency'])
            frequency = int((1000 / frequency) * 1000)
            tone = [pigpio.pulse(1 << pin, 0, frequency),
                    pigpio.pulse(0, 1 << pin, frequency)]

            self.pi.wave_add_generic(tone)
            wid = self.pi.wave_create()

            if wid >= 0:
                self.pi.wave_send_repeat(wid)
                time.sleep(1)
                self.pi.wave_tx_stop()
                self.pi.wave_delete(wid)
        # when a user wishes to outout a DHT11 sensor value
        elif client_cmd == 'temperature':
            pin = int(payload['pin'])
            temp, hum = dht11.read(pin)
            payload = {'report': 'temp_data', 'temp': str(temp), 'hum': str(hum)}
          #  print('callback', payload)
            msg = json.dumps(payload)
            self.sendMessage(msg)
        
        # when a user wishes to outout a Joystick value with PCF8591
        elif client_cmd == 'joystick_read_pcf8591':
            address = payload['channel']
            y_pin = int(payload['y_pin'])
            x_pin = int(payload['x_pin'])
            bt_pin = int(payload['bt_pin'])
            direction = joystick_ps2.read_pcf8591(address, y_pin, x_pin, bt_pin)
            payload = {'report': 'joystick_data', 'direction': str(direction)}
            msg = json.dumps(payload)
            self.sendMessage(msg)   
        
        # when a user wishes to outout a Joystick value with MCP3008
        elif client_cmd == 'joystick_read_mcp3008':
            spi_device = int(payload['spi_device'])
            spi_port = int(payload['spi_port'])
            y_pin = int(payload['y_pin'])
            x_pin = int(payload['x_pin'])
            bt_pin = int(payload['bt_pin'])
            direction = joystick_ps2.read_mcp3008(spi_device, spi_port, y_pin, x_pin, bt_pin)
            payload = {'report': 'joystick_data', 'direction': str(direction)}
            msg = json.dumps(payload)
            self.sendMessage(msg)    
        
        # when a user wishes to write on the lcd1602 display
        elif client_cmd == 'lcd1602_write':
            message = payload['text']
            line = int(payload['line'])
            lcd1602_i2c.write_message(message, line)  
            
        # when a user wishes to outout a BMP180 sensor value
        elif client_cmd == 'bmp_read':
            # bool = int(payload['bool'])
            pressure, altitude = bmp.read_sensor()
            payload = {'report': 'bmp_data', 'pressure': str(pressure), 'altitude': str(altitude)}
            msg = json.dumps(payload)
            self.sendMessage(msg)

        # when a user wishes to output a gas sensor value
        elif client_cmd == 'gas_sensor':
            pin = int(payload['pin'])
            adc = payload['adc']
            # TODO: try_statement for function call / check for gas_data equals zero or null
            gas_data = gas.read(adc, pin)
            payload = {'report': 'gas_data', 'gas_data': str(gas_data)}
            #print('callback', payload)
            msg = json.dumps(payload)
            self.sendMessage(msg)

        # when a user wishes to output a rain sensor value
        elif client_cmd == 'rain_sensor':
            pin = int(payload['pin'])
            adc = payload['adc']
            # TODO: try_statement for function call / check for rain_data ! 0 and...
            rain_data = rain.read(adc, pin)
            payload = {'report': 'rain_data', 'rain_data': str(rain_data)}
            #print('callback', payload)
            msg = json.dumps(payload)
            self.sendMessage(msg) 

        # when a user wishes to output a sound sensor value
        elif client_cmd == 'sound_sensor':
            pin = int(payload['pin'])
            adc = payload['adc']
            # TODO: try_statement for function call / check for sound_data ! 0 and...
            sound_data = sound.read(adc, pin)
            payload = {'report': 'sound_data', 'sound_data': str(sound_data)}
            #print('callback', payload)
            msg = json.dumps(payload)
            self.sendMessage(msg)

        # when a user wishes to output a flame sensor value
        elif client_cmd == 'flame_sensor':
            pin = int(payload['pin'])
            adc = payload['adc']
            # TODO: try_statement for function call / check for flame_data ! 0 and...
            flame_data = flame.read(adc, pin)
            payload = {'report': 'flame_data', 'flame_data': str(flame_data)}
            #print('callback', payload)
            msg = json.dumps(payload)
            self.sendMessage(msg)    
            
            
        elif client_cmd == 'temperature2':
            pin = int(payload['pin'])
            #temp, hum = dht11_pigpio.read(pin)
            #payload = {'report': 'temp_data', 'temp': str(temp), 'hum': str(hum)}
            #print('callback', payload)
            #msg = json.dumps(payload)
            #self.sendMessage(msg)
            self.pi.set_mode(pin, pigpio.OUTPUT)
            self.pi.write(pin, 1)
            
        elif client_cmd == 'ready':
            pass
        else:
            print("Unknown command received", client_cmd)
    
    # call back the dht11 sensor value to scratch
    
    #def dht11_callback(self, temp, hum):
    #    payload = {'report': 'send_temp_data', 'temp': str(temp), 'hum': str(hum)}
   #     print('callback', payload)
   #     msg = json.dumps(payload)
   #     self.sendMessage(msg)

    # call back from pigpio when a digital input value changed
    # send info back up to scratch
    def input_callback(self, pin, level, tick):
        payload = {'report': 'digital_input_change', 'pin': str(pin), 'level': str(level)}
        print('callback', payload)
        msg = json.dumps(payload)
        self.sendMessage(msg)
        
    def input_callback2(self, pin, level, tick):
        payload = {'report': 'digital_write2', 'pin': str(pin), 'level': str(level)}
        print('callback', payload)
        msg = json.dumps(payload)
        self.sendMessage(msg)

    def handleConnected(self):
        self.pi = pigpio.pi()
        print(self.address, 'connected')

    def handleClose(self):
        print(self.address, 'closed')


def run_server():
    # checking running processes.
    # if the backplane is already running, just note that and move on.
    found_pigpio = False

    for pid in psutil.pids():
        p = psutil.Process(pid)
        if p.name() == "pigpiod":
            found_pigpio = True
            print("pigpiod is running")
        else:
            continue

    if not found_pigpio:
        call(['sudo', 'pigpiod'])
        print('pigpiod has been started')

    os.system('scratch2&')
    server = SimpleWebSocketServer('', 9000, S2Gpio)
    server.serveforever()


if __name__ == "__main__":
    try:
        run_server()
    except KeyboardInterrupt:
        sys.exit(0)


