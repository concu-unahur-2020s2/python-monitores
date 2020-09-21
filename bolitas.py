import threading
import time
import logging
import random

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)

class Participante(threading.Thread):
    def __init__(self, monitor):
        super().__init__()
        self.monitor = monitor

    def ponerBolitas(self):
        cantAPoner = random.randint(1, 5)
        contador = 0 

        with self.monitor:
            for i in range(cantAPoner):
                frascoBolitas.append(i)
                self.monitor.notify()
                contador += 1
        logging.info(f'puse {contador} bolitas.')
    
    def sacarBolitas(self):
        cantASacar = random.randint(1, 10)
        contador = 0

        with self.monitor:
            while len(frascoBolitas) < cantASacar:
                logging.info(f'-Intente sacar {cantASacar}-')
                self.monitor.wait()

            while contador < cantASacar:
                frascoBolitas.pop(0)
                contador += 1
        logging.info(f'saque {contador} bolitas.')
        
    def run(self):
        while True:
            self.ponerBolitas()
            time.sleep(random.uniform(1, 3))
            self.sacarBolitas()
            time.sleep(random.uniform(1, 5))

frascoBolitas = []
monitBolitas = threading.Condition()
cantParticipantes = int(input("Ingrese cantidad de participantes:"))

for i in range(cantParticipantes):
    Participante(monitBolitas).start()