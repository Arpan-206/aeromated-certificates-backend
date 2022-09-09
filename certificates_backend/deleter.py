#!/usr/bin/env python3

import os
import threading
def deleter():
    test = os.listdir("certificates/")
    for item in test:
        if item.endswith(".png"):
            os.remove(os.path.join("certificates/", item))


def timed_delete():
    deleter()
  
timer = threading.Timer(1800.0, timed_delete)
timer.start()