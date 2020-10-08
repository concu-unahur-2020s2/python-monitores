import threading
import time
import logging
import random

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)


class Chique(threading.Thread):
    def __init__(self, monitor):
        super().__init__()
        self.monitor = monitor

    #Hago que la cantidad de bolitas a poner/sacar varíe cada vez.
    #Podría haber sido fija, y distinta para cada jugador.
    def cantBolitas(self):
        return random.randint(1,10)

    def sacarBolitas(self):
        cant = self.cantBolitas()
        with self.monitor: # sincronizo para no pisarme con otro thread        
            while len(items) < cant: # si no hay esa cantidad para sacar, espero...
                self.monitor.wait() 
            for _ in range(cant):
                items.pop(0)    
            logging.info(f'Saqué {cant} bolitas. Quedan {len(items)} bolitas')
            time.sleep(2)

    def ponerBolitas(self):
        cant = self.cantBolitas()
        with self.monitor: # sincronizo para no pisarme con otro thread
            for _ in range(cant): # Modelo al frasco con capacidad infinita, asi que no hay condición de espera para poner bolitas.
                items.append(0)
            self.monitor.notify() # notifico para los que están esperando sacar.
            logging.info(f'Puse {cant} bolitas. Quedan {len(items)} bolitas')
            time.sleep(2)

    def run(self):
        while (True):
            caso = random.choice([0,1]) #aleatoriamente saco o pongo
            if(caso == 0):
                self.ponerBolitas()
            else:
                self.sacarBolitas()


cantJugadores = 10

# las bolitas en el frasco la voy a modelar con una lista de ítems.
# Cada elemento de la lista representa una bolita.
# Podría también haber usado una variable que represente la cantidad actual de bolitas en el frasco.
items = []

# El monitor para sincronizar consumir/producir
items_monit = threading.Condition()

# los threads que producen o consumen
for i in range(cantJugadores):
    Chique(items_monit).start() #instancio la clase y lanzo el thread.
