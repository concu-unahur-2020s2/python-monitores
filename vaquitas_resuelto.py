import os
import random
import time
import threading

inicioPuente = 10
largoPuente = 20

cantVacas = 5

semaforoPuente = threading.Semaphore(1) # máximo 1 es por la cantidad al mismo tiempo en el puente

class Vaca(threading.Thread):
  def __init__(self):
    super().__init__()
    self.posicion = 0
    self.velocidad = random.uniform(0.1, 0.9)

  def avanzar(self):
    if (self.posicion == inicioPuente - 1):
        semaforoPuente.acquire()

    time.sleep(1-self.velocidad)
    self.posicion += 1

    if (self.posicion == inicioPuente + largoPuente):
        semaforoPuente.release()
    
  def dibujar(self):
    print(' ' * self.posicion + '🐮') # si no funciona, cambiá por 'V' 

  def run(self):
    while(True):
      self.avanzar()

vacas = []
for i in range(cantVacas):
  v = Vaca()
  vacas.append(v)
  v.start() # si la clase hereda de Thread, el .start() siempre corre run() de la clase.

def cls():
  os.system('cls' if os.name=='nt' else 'clear')

def dibujarPuente():
  print(' ' * inicioPuente + '=' * largoPuente)

while(True):
  cls()
  print('Apretá Ctrl + C varias veces para salir...')
  print()
  dibujarPuente()
  for v in vacas:
    v.dibujar()
  dibujarPuente()
  time.sleep(0.2)
