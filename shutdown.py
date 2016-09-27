#!/usr/bin/env python
import RPi.GPIO as GPIO
import time
import subprocess

GPIO.setmode(GPIO.BOARD)
# set pin 5 to input.  There is a pull-up resistor fitted on the PCB.
GPIO.setup(5, GPIO.IN)

button_counter = 0

# wait for the button to be pressed (input goes low) for 3 seconds
while True:
    time.sleep(.1)

    if not(GPIO.input(5)): # button is pressed
        button_counter += 1
    else: # button is not pressed
        button_counter = 0

    if button_counter > 30: # more than 3 seconds
        break

subprocess.call("/sbin/shutdown -h now &", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

