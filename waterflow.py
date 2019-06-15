#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import sys

TANKINFLOW=35
TANKOUTLET=37
GPIO.setmode(GPIO.BOARD)


GPIO.setup(TANKOUTLET, GPIO.OUT)
GPIO.output(TANKOUTLET, GPIO.HIGH)

GPIO.setup(TANKINFLOW, GPIO.OUT)
GPIO.output(TANKINFLOW, GPIO.HIGH)


flowpin=TANKOUTLET
prompt = "do you want [a]dd or [r]emove water to the plants? (default \'r\') "
flowdirection = raw_input(prompt)
print flowdirection
if ((flowdirection == 'a') or (flowdirection == 'A')):
    flowpin=TANKINFLOW

prompt = "How long should the pump run (default: 2.0)? "
duration = raw_input(prompt)

if not (duration.isdigit()):
    duration=2
else:
    duration=float(duration)
 
print (flowpin)
GPIO.output(flowpin, GPIO.LOW)
time.sleep(duration)
GPIO.output(flowpin, GPIO.HIGH)

GPIO.cleanup()
