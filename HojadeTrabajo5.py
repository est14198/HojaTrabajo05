# HojadeTrabajo5.py
# Algoritmos y Estructura de Datos Seccion 10
# MARIA FERNANDA ESTRADA 14198
# IVETTE MARIA CARDONA 16020
# 26 Febrero 2017

import simpy
import random

intervalo = 10
procesos = 10
random_seed = 10
velocidad_procesador = 1
cant_instrucciones = 3

# El proceso "proceso_OS" muestra el comportamiento del sistema operativo
def proceso_OS (nombre, env, CPU, capacidad_RAM, interval):

    global totalDia
    global tiempoEsperandoRAM
    global saleCPU
    global saleWaiting
    global estadiaCPU
    global enWaiting
    
    # Generador de los procesos
    instrucciones_Faltantes = random.expovariate(1.0/intervalo)
    cant_memoria = random.randint(1,10)

    feew = True

    horaLlegada = env.now

    while (feew):
        if capacidad_RAM.level >= cant_memoria:
            yield capacidad_RAM.get(cant_memoria)
            print ('%s Entro a RAM' % nombre)
            feew = False
        else:
            print('%s Esperando RAM' % nombre)
            tiempoEsperandoRAM = tiempoEsperandoRAM + (env.now-horaLlegada)
            yield env.timeout(1)
            
    # Mientras hayan procesos que realizar, se ejecuta el algoritmo
    while (instrucciones_Faltantes > 1):
        print ('%s Esta en ready' % nombre)
        with CPU.request() as turno:
                yield turno
                entraCPU = env.now
                print ('%s Entro a procesador' % nombre)
                for i in range(cant_instrucciones):
                    yield env.timeout(velocidad_procesador)
                    if (instrucciones_Faltantes <= 1):
                        break
                    else:
                        instrucciones_Faltantes = instrucciones_Faltantes - 1
                saleCPU = env.now-entraCPU
                estadiaCPU = estadiaCPU+saleCPU
                print ('%s Salio del procesador' % (nombre))
        if (instrucciones_Faltantes > 1):
            num = random.randint(1,2)
            if (num == 1):
                entraWaiting = env.now
                print ('%s Entro a waiting' % (nombre))
                yield env.timeout(1)
                saleWaiting = env.now-entraWaiting
                enWaiting = enWaiting + saleWaiting
    print ('%s Terminated' % nombre)
    print ('RAM devuelto: %d' %cant_memoria)
    yield capacidad_RAM.put(cant_memoria)
    totalDia = totalDia + tiempoEsperandoRAM + estadiaCPU + enWaiting
    #totalDia = env.now - horaLlegada
            
env = simpy.Environment()
CPU = simpy.Resource(env, capacity = 1)
capacidad_RAM = simpy.Container(env, capacity=200, init=200)
random.seed(random_seed) #Fijar inicio de random

totalDia = 0
tiempoEsperandoRAM = 0
saleCPU = 0
saleWainting = 0
estadiaCPU = 0
enWaiting = 0

for i in range (procesos):
    env.process(proceso_OS('Proceso %d' % i, env, CPU , capacidad_RAM, intervalo))

env.run()

print "Tiempo promedio es: ", totalDia/procesos
