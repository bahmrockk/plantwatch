#!/usr/bin/python
import RPi.GPIO as GPIO

def pinReset():
    REDLIGHT=38
    BLUELIGHT=40
    WATERCIRCULATION=33
    TANKINFLOW=35
    TANKOUTLET=37
    UNUSED1=31
    UNUSED2=29
    UNUSED3=36

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)


    i=(REDLIGHT,BLUELIGHT,WATERCIRCULATION,TANKINFLOW,TANKOUTLET,UNUSED1,UNUSED2,UNUSED3)

    for i2 in i:
        GPIO.setup(i2, GPIO.OUT)
        #this is overkill. It mirrors what the others script do though.
        GPIO.output(i2, GPIO.HIGH)


    GPIO.cleanup()
