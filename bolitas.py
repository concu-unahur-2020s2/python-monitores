from random import Random
import threading
import time
import logging
import random

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)

frasco = []


class Jugador(threading.Thread):
    def __init__(self, monitor):
        super().__init__
        self.monitor = monitor

    def sacar(self):
        cantidad = random.randrange(1,5)
        cont = None

        with self.monitor:
            while len(frasco) < cantidad:
                logging.info(f'saque {cantidad} bolitas')
                self.monitor.wait()
                
            while cont < cantidad:
                frasco.pop(0)
                cont +=1
                logging.info(f'saque {cantidad} bolitas')

    def poner(self):
        cantidad = random.randrange(1,6)
        cont = None

        with self.monitor:
            for i in range(cantidad):
                frasco.append(i)
                self.monitor.notify()
                cont +=1
            logging.info(f'puse {cantidad} bolitas')



    def run(self):
        while True:
            self.sacar()
            time.sleep(random.uniform(0.5,1.2))
            self.poner()
            time.sleep(random.uniform(0.5,1))

monitor = threading.Condition()
jugadores = 6

for j in range(jugadores):
    Jugador(monitor).start()