#!/usr/bin/python
import RPi.GPIO as GPIO
import sys
import threading


def runFountain(exit, duration):
    WATERCIRCULATION=33
    GPIO.setmode(GPIO.BOARD)

    print "starting fountain for ", duration, " seconds"
    def gracefulQuit():
        print "quitting gracefully the fountain"
        GPIO.output(WATERCIRCULATION, GPIO.HIGH)
        GPIO.cleanup()
        exit.set()
        quit()

    def gracefulSleep(i):
        if i > 0:
            exit.wait(timeout=i)
        if exit.is_set():
            gracefulQuit()
 

    GPIO.setup(WATERCIRCULATION, GPIO.OUT)
    GPIO.output(WATERCIRCULATION, GPIO.LOW)

    gracefulSleep(float(duration))
    gracefulQuit()
    GPIO.cleanup()


if __name__ == "__main__":
    duration = sys.argv[1]
    if not (duration.isdigit()):
            duration = 120

    exit = threading.Event()
    runFountain(exit,duration)
