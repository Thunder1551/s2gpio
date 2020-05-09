#!/usr/bin/env python
import LCD1602
import time

message_begin = '    ' #some blanks for better reading
empty_display = '                ' #16 blanks to empty display

def initialize(channel):
    LCD1602.init(channel, 1)   # init(slave address, background light)
    LCD1602.clear()

def clear():
    LCD1602.clear()
    
# Note: messages with more than 40 symbols will use both lines
def write_single_line_message(message, line, mode, duration):
    # Displays the message on LCD in a moving sequence from right to left
    if mode == 'right_to_left':
        if (len(message_begin + message) < 40):
            mes = (message_begin + message + empty_display)[0:39]
        else:
            mes = (message_begin + message + empty_display)[0:79]
        for i in range(0, len(message) + 5):
            LCD1602.write(0, line, mes)
            mes = mes[1:]
            time.sleep(duration)
    # Displays the message for the given duration
    elif mode == 'normal':
        message = (message + empty_display)[0:15]
        LCD1602.write(0, line, message) 
        time.sleep(duration)
        LCD1602.write(0, line, empty_display) # overwrite line not use LCD1602.clear()
    # Displays the message permanent until it'll be overwritten or cleared (clear())
    # Attention: Display messages for long periods may be harmful to your LCD1602 module
    elif mode == 'permanent':
        message = (message + empty_display)[0:15]
        LCD1602.write(0, line, message) 
        
def write_double_line_message(message_line0, message_line1, mode, duration):
    # Displays the message on LCD in a moving sequence from right to left
    if mode == 'right_to_left':
        # add blanks before and after message plus 
        message0 = (message_begin + message_line0 + empty_display)[0:39]
        message1 = (message_begin + message_line1 + empty_display)[0:39]
        # check for the longer message lenght
        lenght = 0
        if len(message_line0) < len(message_line1):
            length = len(message_line1)
        else:
            length = len(message_line0)
        for i in range(0, length + 1):
            LCD1602.write(0, 0, message0)
            LCD1602.write(0, 1, message1)
            message0 = message0[1:]
            message1 = message1[1:]
            time.sleep(duration)
            
    # Displays the message for the given duration (Note: 16 symbols)
    elif mode == 'normal':
        message0 = (message_line0 + empty_display)[0:15]
        message1 = (message_line1 + empty_display)[0:15]
        LCD1602.write(0, 0, message0)
        LCD1602.write(0, 1, message1)
        time.sleep(duration)
        LCD1602.clear()
        
    # Displays the message permanent until it'll be overwritten or cleared (clear())
    # Attention: Display messages for long periods may be harmful to your LCD1602 module
    elif mode == 'permanent':
        message0 = (message_line0 + empty_display)[0:15]
        message1 = (message_line1 + empty_display)[0:15]
        LCD1602.write(0, 0, message0)
        LCD1602.write(0, 1, message1)
