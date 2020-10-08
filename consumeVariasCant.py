import threading
import time
import logging
import random

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)




def productor(monitor):
    for i in range(30):
        with monitor:          # hace el acquire y al final un release
            items.append(i)    # agrega un ítem
            monitor.notify()   # Notifica que ya se puede hacer acquire
        time.sleep(2) # simula un tiempo de producción


class Consumidor(threading.Thread):
    def __init__(self, monitor):
        super().__init__()
        self.monitor = monitor
    

    def run(self):
        while (True):
            
            with self.monitor:          # Hace el acquire y al final un release    
                while len(items)< cantAConsumir:     # si no hay ítems para consumir
                    self.monitor.wait()  # espera la señal, es decir el notify
                for i in range(cantAConsumir):
                    x = items.pop(0)     # saca (consume) el primer ítem
                    logging.info(f'Consumí {x}')
            time.sleep(1)


# la lista de ítems a consumir
items = []

# El monitor
items_monit = threading.Condition()


consumidores = 5
cantAConsumir = random.randrange(0,10) # consume siempre el mismo rango, no varia en cada thread

# lanzo los consumidores
for c in range(consumidores):
    cons = Consumidor(items_monit)
    cons.start()



# El productor
productor(items_monit)