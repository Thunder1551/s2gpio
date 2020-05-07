import sys
import os
import time
sys.path.append(os.path.abspath("/home/pi/s2gpio-master/s2gpio/modules"))
import lcd1602_i2c

temp = 24
temp = str(temp)
message = 'Temperature: ' + temp + 'C'
message1 = 'Pressure: ' + temp
mode = 'normal'
duration = 3
line = 1

def test_single_line_permanent_mode():
    lcd1602_i2c.initialize(0x27)
    lcd1602_i2c.write_single_line_message(str(message), 0, 'permanent', 3)
    time.sleep(1)
    lcd1602_i2c.write_single_line_message(str(message), 1, 'permanent', 3)
    time.sleep(1)
    lcd1602_i2c.write_single_line_message(str(message1), 0, 'permanent', 3)
    time.sleep(1)
    lcd1602_i2c.clear()

def test_single_double_left_to_right_mode():
    lcd1602_i2c.initialize(0x27)
    lcd1602_i2c.write_double_line_message(str(message), str(message1), 'left_to_right', 3)
    lcd1602_i2c.write_double_line_message(str(message1), str(message1), 'left_to_right', 3)
    lcd1602_i2c.clear()


try:
    test_single_double_left_to_right_mode()
    test_single_line_permanent_mode()
except NameError:
    print("LCD_Clear: Not connected")
except OSError:
    print("not connected or wrong channel")
"""
try:
    #lcd1602_i2c.initialize(0x27)
    #lcd1602_i2c.write_single_line_message(str(message), 0, 'left_to_right', 1)
    #lcd1602_i2c.write_single_line_message(str(message), 0, 'normal', 3)
    #lcd1602_i2c.write_single_line_message(str(message), 0, 'permanent', 3)
   
    #lcd1602_i2c.write_double_line_message(str(message), str(message), 'left_to_right', 3)
    #lcd1602_i2c.write_double_line_message(str(message), str(message), 'normal', 3)
    #lcd1602_i2c.write_double_line_message(str(message), str(message), 'permanent', 3)
    
    #test_single_line_permanent_mode()
    #test_single_double_left_to_right_mode()
    
    #lcd1602_i2c.clear()
except OSError:
    print("not connected or wrong channel")
    """