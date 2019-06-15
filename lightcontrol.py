#!/usr/bin/python

import RPi.GPIO as GPIO
import time
import sys

GPIO.setmode(GPIO.BOARD)
#order left to right
BLUELIGHT= 40
REDLIGHT = 38

i = (REDLIGHT, BLUELIGHT)
for i2 in i:
    try:
        GPIO.setup(i2, GPIO.OUT)
        GPIO.output(i2, GPIO.HIGH)
    except:
        print (i2 , " ERROR: " , sys.exc_info()[0])

GPIO.output(REDLIGHT, GPIO.LOW)
time.sleep(6*60*60) #6h only red,
GPIO.output(BLUELIGHT, GPIO.LOW)
time.sleep(6*60*60) # and 6h both
 
for i2 in i:
    try:
        GPIO.output(i2, GPIO.HIGH)
    except:
        print (i2, "ERROR: " , sys.exec_info()[0])

GPIO.cleanup()
