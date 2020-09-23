import threading
import time
import logging
import random

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)

cantidadDeConsumidores = 3


def productor(monitor):
    print("Voy a producir")
    for i in range(30):
        with monitor:          # hace el acquire y al final un release
            items.append(i)    # agrega un ítem
            monitor.notify()   # Notifica que ya se puede hacer acquire
        time.sleep(2) # simula un tiempo de producción


class Consumidor(threading.Thread):
    def __init__(self, monitor,aConsumir):
        super().__init__()
        self.monitor = monitor
        self.aConsumir = aConsumir

    def run(self):
        semaforoCantidad = threading.Semaphore(self.aConsumir)
        while (True):
            
            with self.monitor:          # Hace el acquire y al final un release    
                while len(items)< self.aConsumir:     
                    self.monitor.wait()  # espera la señal, es decir el notify
                for i in range (self.aConsumir):
                    x = items.pop(0)     # saca (consume) el primer ítem
                    logging.info(f'Consumí {x}')
            time.sleep(1)


# la lista de ítems a consumir
items = []

# El monitor
items_monit = threading.Condition()

# lista de consumidores
lista = []
for c in range(cantidadDeConsumidores):
    lista.append(c)

# arrancan los consumidores
for c in lista:
    aConsumir = random.randrange(2,5,1)
    cons = Consumidor(items_monit,aConsumir)
    cons.start()


# El productor
productor(items_monit)