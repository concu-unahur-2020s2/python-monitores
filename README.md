# Monitores

La idea básica de un monitor es que funciona como un `Lock` pero que puede esperar a una determinada condición:

```python
monitor = threading.Condition()

# Consumir un ítem
with monitor: # hace el acquire (y al final el release)
    while not hay_un_item():
        monitor.wait() # espera hasta que se dé la señal
    consumir_un_item()

# Producir un ítem
with monitor:
    hacer_un_item()
    monitor.notify() # notifica la señal


# Recordar que el with es una forma fácil de hacer acquire y release.
# Hubiera sido lo mismo hacer así:
monitor.acquire():
try:
    hacer_un_item()
    monitor.notify()
finally:
    monitor.releas()
```

El manejo básico de monitores es el siguiente:
```python
monitor = threading.Condition() #crea el monitor. Se le puede pasar como parámetro un Lock en particular
monitor.acquire() # mismo que para semáforos
monitor.release() # mismo que para semáforos
monitor.wait() # esperar hasta recibir señal
monitor.notify() # dar señal a algún thread que está esperando
monitor.notifyAll() # dar señal a todos los threads que están esperando
```

Se puede leer desde acá [python-threading-condition-objects](https://docs.python.org/3/library/threading.html#condition-objects).


## Productor y consumidores
En `prod-cons.py` hay un ejemplo a modo de guía de uso de un monitor. 

1. Miralo un rato y asegurate de entender la traza (línea de tiempo de ejecución).
1. ¿Por qué el thread que consume sigue consumiendo hasta que se acaban los ítems?
    - Porque a medida que el productor produce los items notifica al consumidor que puede consumir.
2. Suponete que hubiera más de un thread consumiendo. ¿Puede haber más de un consumidor consumiendo a la vez? ¿Por qué? ¿En qué parte de código se maneja eso?
    - Si, puede haber mas de un consumidor consumiendo a la vez. Porque Se retiran elementos de una lista que son totalmente independientes y una vez que un hilo lo retiro ya no puede ser accedido por otro hilo pero si uno quiere asegurarse puede implementar un 'lock' al momento de retirar el item de la lista.
1. En comensales hay también un esquema de productor (el cocinero) y de consumidores (los comensales),  ¿cuál o cuáles son las diferencias de comensales respecto a este?
    - La diferencia es que en comensales se resta 1 a una variable, que es un solo recurso y que puede ser accedido por dos hilos a la vez ya que restar/sumar 1 no es una operacion atomica. En este caso el consumidor accede a una lista de recursos que son independientes uno de otro, por lo que no se ven afectados si hay varios hilos retirando items de la lista.
1. Modificá `prod-cons.py` para que haya varios threads consumiendo.
1. Agregá la posibilidad de que haya consumidores que consuman distintas cantidades (y no siempre de a un ítem).
1. Agregá que cada consumidor pueda consumir solamente una vez (la cantidad que corresponda).


## Bolitas
Varios chicos participan de un juego que consiste en poner o sacar bolitas de un frasco.

* La cantidad que sacan o ponen depende de cada participante, y no es siempre la misma.
* El orden en que los participantes sacan o ponen bolitas no importa.
* **Importante:** si un jugador quiere sacar una cierta cantidad de bolitas, y no existe dicha cantidad en el frasco, debe quedar esperando (quizá junto a otros jugadores) a que haya bolitas en el frasco, es decir a que
otros jugadores pongan bolitas, para luego intentar sacar nuevamente (no importa el
orden en que intente sacar nuevamente).

Hacer un script en python `bolitas.py` que mediante threads de participantes que sacan o ponen bolitas, simule el mencionado juego.

