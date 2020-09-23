import threading
import time
import logging
import random

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)

cantidadDeJugadores = 4
tamanioDeFrasco = 50

class Jugadores(threading.Thread):
    def __init__(self, monitor,cantBolitas,sacarOPoner,tamanioDeFrasco):
        super().__init__()
        self.monitor = monitor
        self.cantBolitas = cantBolitas
        self.sacarOPoner = sacarOPoner
        self.tamanioDeFrasco = tamanioDeFrasco
    
    def sacarBolitas(self,cantBolitas):
        with self.monitor:
            while len(bolitas) < self.cantBolitas:
                self.monitor.wait()
            for i in range(cantBolitas):
                bolitas.pop(0)
            logging.info(f'Agarre {self.cantBolitas} en el frasco quedan {len(bolitas)} bolitas')
            time.sleep(1)

    def ponerBolitas(self,cantBolitas):
        with self.monitor:
            while len(bolitas) > self.tamanioDeFrasco:
                self.monitor.notify()
            x = len(bolitas)
            for i in range(x, (x + self.cantBolitas)):
                bolitas.append(0)
            logging.info(f'Agregue  {self.cantBolitas} bolitas - En el frasco quedan  {len(bolitas)} bolitas')
            time.sleep(1)
    
    def run(self):
        while (True):
            if(self.sacarOPoner <= 30):
                self.ponerBolitas(self.cantBolitas)
            else:
                self.sacarBolitas(self.cantBolitas)


# la lista de bolitas a para jugar
bolitas = []

# El monitor
bolitas_monit = threading.Condition()
logging.info(f'En el frasco hay {len(bolitas)} bolitas') 

# lista de jugadores
lista = []
for c in range(cantidadDeJugadores):
    lista.append(c)

# arrancan los jugadores
for j in lista:
    cantInicialBolitas = random.randrange(1,4,1)
    ramdomSacarOPoner= random.randrange(1,50,1)
    chicos = Jugadores(bolitas_monit,cantInicialBolitas,ramdomSacarOPoner,tamanioDeFrasco)
    chicos.start()

