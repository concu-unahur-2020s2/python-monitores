import threading
import time
import logging
import random

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)

cantConsumidores = 5


def productor(monitor):
    for i in range(30):
        with monitor:          # hace el acquire y al final un release
            items.append(i)    # agrega un ítem
            monitor.notify()   # Notifica que ya se puede hacer acquire
        time.sleep(2) # simula un tiempo de producción


class Consumidor(threading.Thread):
    def __init__(self, monitor,cantAConsumir):
        super().__init__()
        self.monitor = monitor
        self.cantAConsumir = cantAConsumir #Agrego la cantidad a consumir a la clase

    def run(self):
        while (True):
            
            with self.monitor:          # Hace el acquire y al final un release    
                while len(items)<self.cantAConsumir:     # si no hay ítems para consumir
                    self.monitor.wait()  # espera la señal, es decir el notify
                for i in range(self.cantAConsumir):
                    x = items.pop(0)     # saca (consume) el primer ítem
                    logging.info(f'Consumí {x}')
            time.sleep(1)


# la lista de ítems a consumir
items = []

# El monitor
items_monit = threading.Condition()


# una lista de consumidores
lista = []
for c in range(cantConsumidores):
    lista.append(c)

# lanzo los consumidores
for c in lista:
    cantAConsumir = random.randrange(3,8,1) #genero un numero ramdom entre 3 y 8.
    cons = Consumidor(items_monit,cantAConsumir)
    cons.start()



# El productor
productor(items_monit)