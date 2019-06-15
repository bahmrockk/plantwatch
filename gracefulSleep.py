#!/usr/bin/python

  def gracefulSleep (exit, i):
        if i > 0:
            if exit.is_set():
                gracefulQuit()
            else:
                exit.wait(1)
                gracefulSleep(i-1)



