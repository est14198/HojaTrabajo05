# HojadeTrabajo5.py
# Algoritmos y Estructura de Datos Seccion 10
# MARIA FERNANDA ESTRADA 14198
# IVETTE MARIA CARDONA 16020
# 26 Febrero 2017



import simpy
import random

# Variables
intervalo = 10
random_seed = 10
velocidad_procesador = 1
cant_instrucciones = 3

# El proceso "proceso_OS" muestra el comportamiento del sistema operativo
def proceso_OS (nombre, env, CPU, capacidad_RAM, interval):

    global totalDia
    global total2
    
    # Generador de los procesos
    instrucciones_Faltantes = random.expovariate(1.0/intervalo)
    cant_memoria = random.randint(1,10)

    feew = True

    tiempo = env.now

    # Se solicita memoria RAM para poder ir al estado ready
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
        # Solicita al CPU ingresar
        with CPU.request() as turno:
                yield turno
                print ('%s Entro a procesador' % nombre)
                tiempoTotal = env.now - tiempo
                for i in range(cant_instrucciones):
                    yield env.timeout(velocidad_procesador)
                    if (instrucciones_Faltantes <= 1):
                        break
                    else:
                        instrucciones_Faltantes = instrucciones_Faltantes - 1
                print ('%s Salio del procesador %d' % (nombre, tiempoTotal))
                total1 = env.now - tiempoTotal
        if (instrucciones_Faltantes > 1):
            num = random.randint(1,2)
            # Se envia la instruccion a Waiting
            if (num == 1):
                print ('%s Entro a waiting %d' % (nombre, total1))
                total2 = env.now - total1
                yield env.timeout(1)
    # Termina el proceso
    totalDia = totalDia + total2 
    print ('%s Terminated' % nombre)
    print ('RAM devuelto: %d' %cant_memoria)
    yield capacidad_RAM.put(cant_memoria)
            
env = simpy.Environment()
CPU = simpy.Resource(env, capacity = 1)
capacidad_RAM = simpy.Container(env, 100, init=100)
random.seed(random_seed) #Fijar inicio de random

totalDia = 0

for i in range (10):
    env.process(proceso_OS('Proceso %d' % i, env, CPU , capacidad_RAM, intervalo))
env.run()

print "Tiempo promedio es: ", totalDia/10.0
