# HojadeTrabajo5.py
# Algoritmos y Estructura de Datos Seccion 10
# MARIA FERNANDA ESTRADA 14198
# IVETTE MARIA CARDONA 16020
# 1 Marzo 2017



import simpy
import random

# Variables
intervalo = 1
random_seed = 10
velocidad_procesador = 1
cant_instrucciones = 3
cantidad = 200

# El proceso "procesos" determina cuantos procesos se envian al algoritmo
def procesos (env, CPU, capacidad_RAM, interval):
    for i in range(cantidad):
        env.process(OS('Proceso %d' % i, env, CPU , capacidad_RAM))
        t = random.expovariate(1.0/interval)
        yield env.timeout(t)

# El proceso "OS" muestra el comportamiento del sistema operativo
def OS (nombre, env, CPU, capacidad_RAM):

    global totalDia
    global total2

    # Cuanta memoria utilizara
    instrucciones_Faltantes = random.randint(1,10)
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
    while (instrucciones_Faltantes > 0):
        print ('%s Esta en ready' % nombre)
        # Solicita al CPU ingresar
        with CPU.request() as turno:
                yield turno
                print ('%s Entro a procesador' % nombre)
                yield env.timeout(velocidad_procesador)
                instrucciones_Faltantes = instrucciones_Faltantes - cant_instrucciones
                print ('%s Salio del procesador' % (nombre))
        if (instrucciones_Faltantes > 0):
            num = random.randint(1,2)
            # Se envia la instruccion a Waiting
            if (num == 1):
                print ('%s Entro a waiting' % (nombre))
                yield env.timeout(1)
    # Termina el proceso
    totalDia = totalDia + env.now - tiempo
    print ('%s Terminated' % nombre)
    print ('RAM devuelto: %d' %cant_memoria)
    yield capacidad_RAM.put(cant_memoria)

# Se crea la simulacion 
env = simpy.Environment()
CPU = simpy.Resource(env, capacity = 1)
capacidad_RAM = simpy.Container(env,100, init=100)
random.seed(random_seed) #Fijar inicio de random

totalDia = 0

env.process(procesos(env, CPU, capacidad_RAM, intervalo))
env.run()

print "Tiempo promedio es: ", totalDia/cantidad
