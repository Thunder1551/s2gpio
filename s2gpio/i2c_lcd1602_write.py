#!/usr/bin/env python
import LCD1602
import time

def setup():
    LCD1602.init(0x27, 1)   # init(slave address, background light)
    LCD1602.write(0, 0, 'Greetings!!')
    LCD1602.write(1, 1, 'from SunFounder')
    time.sleep(2)

def loop():
    space = '                '
    greetings = 'Thank you for buying SunFounder Sensor Kit for Raspberry! ^_^'
    greetings = space + greetings
    while True:
        tmp = greetings
        for i in range(0, len(greetings)):
            LCD1602.write(0, 0, tmp)
            tmp = tmp[1:]
            time.sleep(0.2)
            LCD1602.clear()

def destroy():
    pass    

if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except KeyboardInterrupt:
        destroy()

# TODO: Enable different modes
def write_message(message, line):
    LCD1602.init(0x27, 1)   # init(slave address, background light)
    mes = '    '
    mes = mes + message
    for i in range(0, len(mes)):
        LCD1602.write(0, line, mes)
        mes = mes[1:]
        time.sleep(0.5)
        LCD1602.clear()