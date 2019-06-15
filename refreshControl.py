#!/usr/bin/python
import RPi.GPIO as GPIO
import sys
import threading
import math

def roundup(x):
    return int(math.ceil(x / 10.0)) * 10

def startRefresh(exit, duration): 
  
    TANKINFLOW=35
    TANKOUTLET=37
    FOUNTAIN=33
    GPIO.setmode(GPIO.BOARD)
    intervalLength = 5

    GPIO.setup(TANKOUTLET, GPIO.OUT)
    GPIO.output(TANKOUTLET, GPIO.HIGH)

    GPIO.setup(FOUNTAIN, GPIO.OUT)
    GPIO.output(FOUNTAIN, GPIO.HIGH)

    GPIO.setup(TANKINFLOW, GPIO.OUT)
    GPIO.output(TANKINFLOW, GPIO.HIGH)


    print "starting refresh cycle"
    def gracefulQuit():
        print "quitting gracefully the refresh cycle"
        GPIO.output(TANKINFLOW, GPIO.HIGH)
        GPIO.output(TANKOUTLET, GPIO.HIGH)
        GPIO.output(FOUNTAIN, GPIO.HIGH)
        GPIO.cleanup()
        exit.set()
        quit()

    if (duration < 30):
        duration = 30

    duration = roundup(duration)
    # one time inflow, one time outflow, four times fountain
    loops=duration/(intervalLength*6)

    def gracefulSleep (i):
        if i > 0:
            exit.wait(i)
        if exit.is_set():
            gracefulQuit()
    
    for x in range (0, loops):
        GPIO.output(TANKOUTLET, GPIO.LOW)
        gracefulSleep(intervalLength)
        GPIO.output(TANKOUTLET, GPIO.HIGH)
        GPIO.output(TANKINFLOW, GPIO.LOW)
        gracefulSleep(intervalLength)
        GPIO.output(TANKINFLOW, GPIO.HIGH)
        GPIO.output(FOUNTAIN, GPIO.LOW)
        gracefulSleep(intervalLength*4)
        GPIO.output(FOUNTAIN, GPIO.HIGH)

    gracefulQuit()


if __name__ == "__main__":
    exit = threading.Event()
    startRefresh(exit, 1)


'''####
    for i in range (0,frequency):
        GPIO.output(TANKOUTLET, GPIO.LOW)
        time.sleep(25)
        GPIO.output(TANKOUTLET, GPIO.HIGH)

        #refresh in smaller chunks
        for i2 in range (0,4):
            
            GPIO.output(FOUNTAIN, GPIO.LOW)
            time.sleep(30)
            GPIO.output(FOUNTAIN, GPIO.HIGH)

            GPIO.output(TANKINFLOW, GPIO.LOW)
            time.sleep(4.95)
            GPIO.output(TANKINFLOW, GPIO.HIGH)
            
     
    GPIO.output(FOUNTAIN, GPIO.LOW)
    time.sleep(60)
    GPIO.output(FOUNTAIN, GPIO.HIGH)

    GPIO.cleanup()



if (len(sys.argv) == 2):
    frequency=sys.argv[1]
    if (frequency.isdigit()):
        startRefresh(int(frequency))
 '''
    
#i = (33)
#for i2 in i:
#    print i2
#    try:
#        GPIO.setup(i2, GPIO.OUT)
#        GPIO.output(i2, GPIO.LOW)
#        time.sleep(2)
#        GPIO.cleanup()
#    except:
#        print (i2 , " ERROR: " , sys.exc_info()[0])
