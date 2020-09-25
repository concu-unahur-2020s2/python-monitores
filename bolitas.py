import threading
import time
import logging
import random

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)

frasco = []

def frasco(monitor):
    for i in range(50):
        with monitor:
            frasco.append(i)
            monitor.notify()
        time.sleep(2)

class Jugador(threading.Thread):
    def __init__(self, monitor):
        super().__init__()
        self.monitor = monitor

    def sacar(self,cantidad):
        
    def run(self):
