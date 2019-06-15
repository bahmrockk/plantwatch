#!/usr/bin/python
import paho.mqtt.client as mqtt
import time 
from refreshControl import startRefresh
from pinreset import pinReset
from fountainControl import runFountain
import threading
#import daemon



exit=threading.Event()
exit.clear()
locked=False

def getIntPayload(message):
    payload = message.payload.decode("utf-8")
    if (payload.isdigit()):
        payload = int(payload)
        print("received payload: ", payload)
    else:
        print("received invalid payload. Defaulting to 0: ", payload)
        payload=0
    return payload


def on_message(client, userdata, message):
    global locked
    topic=message.topic.split("/")

    print("running for topic: ", topic[-1])
    print("exit.set(): ", exit.is_set())
    print("locked: ", locked)
    if(topic[-1] == "interrupt"):
        exit.set() 
   
    '''
    Check if the last thread was fininshed.
    The cleanup and check happens right before a new event fires. 
    This is just to make sure that each thread has a clean start.
    Only when the interrupt is triggered is timing critical.
    '''

    if (exit.is_set()):
        #give all threads plenty of time to do their thing with the exit-flag
        time.sleep(2)
        pinReset()
        exit.clear()
        locked=False
    
    if (not locked):
        payload=getIntPayload(message)
        myArgs=(exit,payload)
        threadOptions = {
            "refreshCycle": threading.Thread(target=startRefresh, args=myArgs),
            "fountain": threading.Thread(target=runFountain, args=myArgs)
        }
        thread=threadOptions.get(topic[-1], None)

        if (thread is not None):
            print("Starting thread: ", topic[-1], " with payload: ", payload)
            locked=True
            thread.start()
        else:
            print("Unknown event received: ", topic[-1])

def listen():
    client = mqtt.Client()
    client.on_message=on_message
    client.connect("192.168.1.4")
    #client.subscribe([("plantwatch/refreshCycle",2),("plantwatch/interrupt",2),("test/test",0)])
    
    client.subscribe("plantwatch/+",2)
    client.loop_forever()

if __name__ == "__main__":
    listen()

#with daemon.DaemonContext():
#    listen()
