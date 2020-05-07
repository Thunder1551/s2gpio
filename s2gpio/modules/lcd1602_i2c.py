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
    
# TODO: Enable different modes
def write_single_line_message(message, line, mode, duration):
    # Displays the message on LCD from left to right
    if mode == 'left_to_right':
        mes = message_beginn + message
        for i in range(0, len(mes)):
            LCD1602.write(0, line, mes + empty_display)
            mes = mes[1:]
            time.sleep(0.5)
            LCD1602.clear()
    # Displays the message for the given duration
    elif mode == 'normal':
        LCD1602.write(0, line, message + empty_display) # blanks added to for overwriting previous message
        time.sleep(duration)
        LCD1602.clear()
    # Displays the message solid until it'll be overwritten
    elif mode == 'permanent':
        LCD1602.write(0, line, message + empty_display) # blanks added to for overwriting previous message
        
def write_double_line_message(message_line0, message_line1, mode, duration):
    # Displays the message on LCD from left to right
    if mode == 'left_to_right':
        message0 = message_begin + message_line0
        message1 = message_begin + message_line1
        # check for the longer message lenght
        lenght = 0
        if len(message0) < len(message1):
            lenght = len(message1)
        else:
            lenght = len(message0)
        for i in range(0, lenght):
            LCD1602.write(0, 0, message0 + empty_display)
            LCD1602.write(0, 1, message1 + empty_display)
            message0 = message0[1:]
            message1 = message1[1:]
            time.sleep(0.5)
            
    # Displays the message for the given duration (Note: 16 symbols)
    elif mode == 'normal':
        LCD1602.write(0, 0, message_line0 + empty_display) # blanks added to for overwriting previous message
        LCD1602.write(0, 1, message_line1 + empty_display) # blanks added to for overwriting previous message
        time.sleep(duration)
        LCD1602.clear()
        
    # Displays the message permanent until it'll be overwritten or cleared (clear())
    # Attention: not clearing may be harmful to your LCD1602 module
    elif mode == 'permanent':
        LCD1602.write(0, 0, message_line0 + empty_display) # blanks added to for overwriting previous message
        LCD1602.write(0, 1, message_line1 + empty_display) # blanks added to for overwriting previous message