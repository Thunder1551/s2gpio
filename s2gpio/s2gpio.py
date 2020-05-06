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
sys.path.append(os.path.abspath("/home/pi/s2gpio-master/s2gpio/modules"))
import analog_hall
import bmp
import dht11
import flame
import gas
import joystick_ps2
import lcd1602_i2c
import photoresistor
import rain
import sound
import thermistor

import time
import datetime
from subprocess import call
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
        
        # when a user wants to read a sensor module connect to i2c
        elif client_cmd == 'i2c_read':
            sensor = payload['model']
            channel = payload['channel']
            if sensor == 'BMP180':
                try:
                    pressure, altitude = bmp.read_sensor()
                    payload = {'report': 'bmp_return', 'bmp_pressure': str(pressure), 'bmp_altitude': str(altitude)}
                    msg = json.dumps(payload)
                    self.sendMessage(msg)
                except OSError:
                    print("Not connected or wrong channel")
        
        # when a user wants to read a PS2 Joystck with PCF8591 module
        elif client_cmd == 'joystick_read':
            #direction = joystick_ps2.read_pcf8591(0x48, y_pin, x_pin, bt_pin)
            value = joystick_ps2.read_PCF8591(0x48,3,2,1)
            payload = {'report': 'joystick_return', 'joystick_data': str(value)}
            msg = json.dumps(payload)
            self.sendMessage(msg)
        
        # when a user wants to read a PS2 Joystck with PCF8591 module
        elif client_cmd == 'joystick_read_pcf8591':
            y_pin = int(payload['y_pin'])
            x_pin = int(payload['x_pin'])
            bt_pin = int(payload['bt_pin'])
            try:
                direction = joystick_ps2.read_PCF8591(0x48, y_pin, x_pin, bt_pin)
                payload = {'report': 'joystick_return', 'joystick_data': str(direction)}
                msg = json.dumps(payload)
                self.sendMessage(msg)
            except OSError:
                print("Not connected or wrong channel")
                    
        # when a user wants to read an analog sensor value with PCF8591 module
        elif client_cmd == 'pcf_read':
            pin = int(payload['a_pin'])
            model = payload['model']
            try:
                if model == 'Flame':
                    sensor_value = flame.read_PCF8591(0x48, pin)
                    payload = {'report': 'flame_return', 'flame_data': str(sensor_value)}
                elif model == 'Gas':
                    sensor_value = gas.read_PCF8591(0x48, pin)
                    payload = {'report': 'gas_return', 'gas_data': str(sensor_value)}
                elif model == 'Hall':
                    sensor_value = analog_hall.read_PCF8591(0x48, pin)
                    payload = {'report': 'hall_return', 'hall_data': str(sensor_value)}
                elif model == 'Photoresistor':
                    sensor_value = photoresistor.read_PCF8591(0x48, pin)
                    payload = {'report': 'photoresistor_return', 'photoresistor_data': str(sensor_value)}
                elif model == 'Rain':
                    sensor_value = rain.read_PCF8591(0x48, pin)
                    payload = {'report': 'rain_return', 'rain_data': str(sensor_value)}
                elif model == 'Sound':
                    sensor_value = sound.read_PCF8591(0x48, pin)
                    payload = {'report': 'sound_return', 'sound_data': str(sensor_value)}
                elif model == 'Thermistor':
                    sensor_value = gas.read_PCF8591(0x48, pin)
                    payload = {'report': 'thermistor_return', 'thermistor_data': str(sensor_value)}
                msg = json.dumps(payload)
                self.sendMessage(msg)
            except OSError:
                print("Not connected or wrong channel")
            
        elif client_cmd == 'ready':
            pass
        else:
            print("Unknown command received", client_cmd)

    # call back from pigpio when a digital input value changed
    # send info back up to scratch
    def input_callback(self, pin, level, tick):
        payload = {'report': 'digital_input_change', 'pin': str(pin), 'level': str(level)}
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


