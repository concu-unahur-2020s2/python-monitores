import threading
import time
import logging
import random

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)

cantChicos = 10
tamaniaDeFrascoEnBolitas = 100

class Chicos(threading.Thread):
    def __init__(self, monitor, cantBolitas, sacarOPoner,tamaniaDeFrascoEnBolitas):
        super().__init__()
        self.monitor = monitor
        self.cantBolitas = cantBolitas 
        self.sacarOPoner = sacarOPoner
        self.tamaniaDeFrascoEnBolitas = tamaniaDeFrascoEnBolitas

    def sacarBolitas(self,cantBolitas):
        with self.monitor:         
            while len(items) < self.cantBolitas:   
                self.monitor.wait() 
            for i in range(self.cantBolitas):
                items.pop(0)    
            logging.info(f'Saque {self.cantBolitas} bolitas - Quedan en el frasco {len(items)} bolitas')
            time.sleep(1)

    def ponerBolitas(self,cantBolitas):
        with self.monitor:
            while len(items) > self.tamaniaDeFrascoEnBolitas:
                self.monitor.notify()
            x = len(items)
            for i in range(x, (x + self.cantBolitas)):
                items.append(0)
            logging.info(f'Puse {self.cantBolitas} bolitas - Quedan en el frasco {len(items)} bolitas')
            time.sleep(1)

    def run(self):
        while (True):
            if(self.sacarOPoner <= 50):
                self.ponerBolitas(self.cantBolitas)
            else:
                self.sacarBolitas(self.cantBolitas)


# la lista de ítems a consumir
items = []

# El monitor
items_monit = threading.Condition()
logging.info(f'En el frasco hay {len(items)} bolitas')

# una lista de chicos
lista = []
for p in range(cantChicos):
    lista.append(p)

# suelto a los pibes
for p in lista:
    cantInicBolitas = random.randrange(1,5,1)
    ramdomSacarOPoner= random.randrange(1,100,1)
    pibitos = Chicos(items_monit,cantInicBolitas,ramdomSacarOPoner,tamaniaDeFrascoEnBolitas)
    pibitos.start()

