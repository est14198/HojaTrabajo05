# HojadeTrabajo5.py
# Algoritmos y Estructura de Datos Seccion 10
# MARIA FERNANDA ESTRADA 14198
# IVETTE MARIA CARDONA 16020
# 26 Febrero 2017

import simpy
import random
import time

intervalo = 10
random_seed = 10
velocidad_procesador = 1
cant_instrucciones = 3

class Timer(object):
    def __init__(self, verbose=False):
        self.verbose = verbose

    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, *args):
        self.end = time.time()
        self.secs = self.end - self.start
        self.msecs = self.secs * 1000  # millisecs
        if self.verbose:
            print 'elapsed time: %f ms' % self.msecs

# El proceso "proceso_OS" muestra el comportamiento del sistema operativo
def proceso_OS (nombre, env, CPU, capacidad_RAM, interval):
    
    # Generador de los procesos
    instrucciones_Faltantes = random.expovariate(0.1/intervalo)
    cant_memoria = random.randint(1,10)

    feew = True

    while (feew):
        if capacidad_RAM.level >= cant_memoria:
            yield capacidad_RAM.get(cant_memoria)
            print ('%s Entro a RAM' % nombre)
            feew = False
        else:
            print('%s Esperando RAM' % nombre)
            yield env.timeout(1)
            
    # Mientras hayan procesos que realizar, se ejecuta el algoritmo
    while (instrucciones_Faltantes > 1):
        print ('%s Esta en ready' % nombre)
        with CPU.request() as turno:
                yield turno
                print ('%s Entro a procesador' % nombre)
                for i in range(cant_instrucciones):
                    yield env.timeout(velocidad_procesador)
                    if (instrucciones_Faltantes <= 1):
                        break
                    else:
                        instrucciones_Faltantes = instrucciones_Faltantes - 1
                print ('%s Salio del procesador' % nombre)
        if (instrucciones_Faltantes > 1):
            num = random.randint(1,2)
            if (num == 1):
                print ('%s Entro a waiting' % nombre)
                yield env.timeout(1)
    print ('%s Terminated' % nombre)
    print ('RAM devuelto: %d' %cant_memoria)
    yield capacidad_RAM.put(cant_memoria)
            

env = simpy.Environment()
CPU = simpy.Resource(env, capacity = 1)
capacidad_RAM = simpy.Container(env, 100, init=10)
random.seed(random_seed) #Fijar inicio de random 
for i in range (10):
    env.process(proceso_OS('Proceso %d' % i, env, CPU , capacidad_RAM, intervalo))
env.run()
