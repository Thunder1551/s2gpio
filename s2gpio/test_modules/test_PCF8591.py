import time

import sys
import os
sys.path.append(os.path.abspath("/home/pi/s2gpio-master/s2gpio/modules"))
import analog_hall
import PCF8591 as ADC
import RPi.GPIO as GPIO

ADC.setup(0x48)
print('Reading PCF8591 raw values, press Ctrl-C to quit...')
# Print nice channel column headers.
print('| {0:>4} | {1:>4} | {2:>4} | {3:>4} |'.format(*range(4)))
print('-' * 57)
# Main program loop.
while True:
    # Read all the ADC channel values in a list.
    values = [0]*8
    for i in range(4):
        # The read function will get the raw value of the specified channel (0-3).
        values[i] = ADC.read(i)
    # Print the ADC values.
    print('| {0:>4} | {1:>4} | {2:>4} | {3:>4} |'.format(*values))
    # Pause for half a second.
    time.sleep(0.5)