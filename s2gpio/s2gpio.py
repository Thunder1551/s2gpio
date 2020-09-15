#!/usr/bin/env python3

"""
 Copyright (c) 2020 Chris Hammerschmidt All rights reserved.
 
 Note: The basic structure was taken over by Alan Yoricks. The rights to this code remain exclusively with Alan Yoricks.
 All changes made to the program code are clearly marked with "***RoboRasp --->". If not explicitly marked, the code remains under the following copyright:
 
 Copyright (c) 2016-2018 Alan Yorinks All rights reserved.
 
 For information about the original project with related documentation please refer to
 https://github.com/MrYsLab/s2-pi
 https://mryslab.github.io/s2-pi/
 
 
 This program is free software; you can redistribute it and/or
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
from subprocess import call

# ***RoboRasp ---> Begin of added import commands
import datetime
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
# ***RoboRasp ---> End of added import commands

import pigpio
import psutil
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket


# This class inherits from WebSocket.
# It receives messages from the Scratch and reports back for any digital input
# changes.
class S2Pi(WebSocket):

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
        elif client_cmd == 'ready':
            pass
        else:
            print("Unknown command received", client_cmd)
       
        """
        ***RoboRasp ---> Begin of handling client messages 
        dht11_read
        lcd_initialize
        lcd_clear
        lcd_single_line
        lcd_double_line
        i2c_read
        pcf_read
        mcp_read
        joystick_read_pcf8591
        """
        # when a user wants to initialize a LCD1602 display
        elif client_cmd == 'lcd_initialize':
            channel = payload['channel']
            try:
                lcd1602_i2c.initialize(int(channel, 16)) # call outsourced read dunction
            except OSError:
                print("lcd_initialize: Display not connected or wrong channel")
        
        
        # when a user wants to clear a LCD1602 display
        elif client_cmd == 'lcd_clear':
            try:
                lcd1602_i2c.clear() # call outsourced read dunction
            except NameError:
                print("lcd_clear: Display not initialized")
                
        # when a user wants to display a single-line message on LCD1602
        elif client_cmd == 'lcd_single_line':
            message = payload['message']
            line = int(payload['line'])
            mode = payload['mode']
            duration = int(payload['duration'])
            try:
                lcd1602_i2c.write_single_line_message(str(message), line, mode, duration) # call outsourced read dunction
            except NameError:
                print("lcd_single_line: Display not initialized")
            except ValueError:
                print("lcd_single_line: Input for duration was not an int or float")
                
        # when a user wants to display a double-line message on LCD1602
        elif client_cmd == 'lcd_double_line':
            message0 = payload['message0']
            message1 = payload['message1']
            mode = payload['mode']
            duration = int(payload['duration'])
            try:
                lcd1602_i2c.write_double_line_message(str(message0), str(message1), mode, duration) # call outsourced read dunction
            except NameError:
                print("lcd_double_line: Display not initialized")
            except ValueError:
                print("lcd_double_line: Input for duration was not an int or float")
        
        # when a user wants to read a sensor module connect to i2c
        elif client_cmd == 'i2c_read':
            sensor = payload['model']
            channel = payload['channel']
            try:
                if sensor == 'BMP180':
                    pressure, altitude = bmp.read_sensor() # call outsourced read dunction
                    payload = {'report': 'bmp_return', 'bmp_pressure': str(pressure), 'bmp_altitude': str(altitude)}
                    msg = json.dumps(payload)
                    self.sendMessage(msg)
            except OSError:
                print("I2C_Read: Chosen sensor not connected or wrong channel")
 
        # when a user wants to read an analog sensor value with PCF8591 module
        elif client_cmd == 'pcf_read':
            pin = int(payload['a_pin'])
            model = payload['model']
            try:
                if model == 'Flame':
                    sensor_value = flame.read_PCF8591(0x48, pin) # call outsourced read dunction
                    payload = {'report': 'flame_return', 'flame_data': str(sensor_value)}
                elif model == 'Gas':
                    sensor_value = gas.read_PCF8591(0x48, pin) # call outsourced read dunction
                    payload = {'report': 'gas_return', 'gas_data': str(sensor_value)}
                elif model == 'Hall':
                    sensor_value = analog_hall.read_PCF8591(0x48, pin) # call outsourced read dunction
                    payload = {'report': 'hall_return', 'hall_data': str(sensor_value)}
                elif model == 'Photoresistor':
                    sensor_value = photoresistor.read_PCF8591(0x48, pin) # call outsourced read dunction
                    payload = {'report': 'photoresistor_return', 'photoresistor_data': str(sensor_value)}
                elif model == 'Rain':
                    sensor_value = rain.read_PCF8591(0x48, pin) # call outsourced read dunction
                    payload = {'report': 'rain_return', 'rain_data': str(sensor_value)}
                elif model == 'Sound':
                    sensor_value = sound.read_PCF8591(0x48, pin) # call outsourced read dunction
                    payload = {'report': 'sound_return', 'sound_data': str(sensor_value)}
                elif model == 'Thermistor':
                    sensor_value = gas.read_PCF8591(0x48, pin) # call outsourced read dunction
                    payload = {'report': 'thermistor_return', 'thermistor_data': str(sensor_value)}
                msg = json.dumps(payload)
                self.sendMessage(msg)
            except OSError:
                print("PCF_Read: Chosen sensor not connected or wrong channel")
              
        # when a user wants to read an analog sensor value with MCP3008 module
        elif client_cmd == 'mcp_read':
            pin = int(payload['a_pin'])
            model = payload['model']
            try:
                if model == 'Flame':
                    sensor_value = flame.read_MCP3008(0, 0, pin) # call outsourced read dunction
                    payload = {'report': 'flame_return', 'flame_data': str(sensor_value)}
                elif model == 'Gas':
                    sensor_value = gas.read_MCP3008(0, 0, pin) # call outsourced read dunction
                    payload = {'report': 'gas_return', 'gas_data': str(sensor_value)}
                elif model == 'Hall':
                    sensor_value = analog_hall.read_MCP3008(0, 0, pin) # call outsourced read dunction
                    payload = {'report': 'hall_return', 'hall_data': str(sensor_value)}
                elif model == 'Photoresistor':
                    sensor_value = photoresistor.read_MCP3008(0, 0, pin) # call outsourced read dunction
                    payload = {'report': 'photoresistor_return', 'photoresistor_data': str(sensor_value)}
                elif model == 'Rain':
                    sensor_value = rain.read_MCP3008(0, 0, pin) # call outsourced read dunction
                    payload = {'report': 'rain_return', 'rain_data': str(sensor_value)}
                elif model == 'Sound':
                    sensor_value = sound.read_MCP3008(0, 0, pin) # call outsourced read dunction
                    payload = {'report': 'sound_return', 'sound_data': str(sensor_value)}
                elif model == 'Thermistor':
                    sensor_value = thermistor.read_MCP3008(0, 0, pin) # call outsourced read dunction
                    payload = {'report': 'thermistor_return', 'thermistor_data': str(sensor_value)}
                msg = json.dumps(payload)
                self.sendMessage(msg)
            except OSError:
                print("PCF_Read: Chosen sensor not connected or wrong channel")
              
              
        # when a user wants to read a PS2 Joystick with PCF8591 module
        elif client_cmd == 'joystick_read_pcf8591':
            y_pin = int(payload['y_pin'])
            x_pin = int(payload['x_pin'])
            bt_pin = int(payload['bt_pin'])
            try:
                direction = joystick_ps2.read_PCF8591(0x48, y_pin, x_pin, bt_pin) # call outsourced read dunction
                payload = {'report': 'joystick_return', 'joystick_data': str(direction)}
                msg = json.dumps(payload)
                self.sendMessage(msg)
            except OSError:
                print("Joystick_Read_PCF8591: Not connected or wrong channel")
              
        # ***RoboRasp ---> End of handling client messages 
            
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
    server = SimpleWebSocketServer('', 9000, S2GPIO)
    server.serveforever()


if __name__ == "__main__":
    try:
        run_server()
    except KeyboardInterrupt:
        sys.exit(0)
