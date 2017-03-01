# HojadeTrabajo5.py
# Algoritmos y Estructura de Datos Seccion 10
# MARIA FERNANDA ESTRADA 14198
# IVETTE MARIA CARDONA 16020
# 26 Febrero 2017



import simpy
import random

# El proceso "proceso_OS" muestra el comportamiento del sistema operativo
def proceso_OS (nombre, env, CPU, capacidad_RAM):

    velocidad_procesador = 1
    cant_instrucciones = 3
    
    # Generador de los procesos
    instrucciones_Faltantes = random.expovariate(1.0/10)
    cant_memoria = random.randint(1,10)

    feew = True

    # Sigue en proceso si hay espacio en RAM, sino espera un turno hasta que este disponible
    while (feew):
        if capacidad_RAM.level >= cant_memoria:
            yield capacidad_RAM.get(cant_memoria)
            print ('%s Entro a RAM' % nombre)
            feew = False
        else:
            print('%s Esperando RAM' % nombre)
            yield env.timeout(1)
            
    # Mientras hayan procesos que realizar, se ejecuta el algoritmo
    while (instrucciones_Faltantes != 0):
        print ('%s Esta en ready' % nombre)
        # Solicita turno al CPU
        with CPU.request() as turno:
                yield turno
                print ('%s Entro a procesador' % nombre)
                for i in range(cant_instrucciones):
                    yield env.timeout(velocidad_procesador)
                    if (instrucciones_Faltantes == 0):
                        break
                    else:
                        instrucciones_Faltantes = instrucciones_Faltantes - 1
                print ('%s Salio del procesador' % nombre)
        if (instrucciones_Faltantes > 0):
            num = random.randint(1,2)
            if (num == 1):
                print ('%s Entro a waiting' % nombre)
                yield env.timeout(1)
    print ('%s Terminated' % nombre)
    print ('RAM devuelto: %d' %cant_memoria)
    yield capacidad_RAM.put(cant_memoria)
            


    
# Simulacion
env = simpy.Environment()
CPU = simpy.Resource(env, capacity = 1)
capacidad_RAM = simpy.Container(env, 100, init=100)
random.seed(10)
for i in range (10):
    env.process(proceso_OS('Proceso %d' % i, env, CPU , capacidad_RAM))
env.run()
