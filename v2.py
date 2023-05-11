import concurrent.futures
import random
import time
import threading

# Clase Fumador
class Fumador:
    def __init__(self, nombre, ingrediente1, ingrediente2):
        self.nombre = nombre
        self.ingrediente1 = ingrediente1
        self.ingrediente2 = ingrediente2

    def fumar(self):
        print(f"Fumador {self.nombre} está fumando.")
        time.sleep(2)  # Simulamos el tiempo que tarda en fumar
        print(f"Fumador {self.nombre} ha terminado de fumar.")

# Clase Agente
class Agente:
    def __init__(self):
        self.mutex = threading.Semaphore(1)
        self.tabaco_sem = threading.Semaphore(0)
        self.papel_sem = threading.Semaphore(0)
        self.fosforos_sem = threading.Semaphore(0)

    def colocar_ingredientes(self):
        while True:
            self.mutex.acquire()
            ingredientes = random.sample(["tabaco", "papel", "fosforos"], 2)
            if "tabaco" in ingredientes and "papel" in ingredientes:
                self.fosforos_sem.release()
            elif "tabaco" in ingredientes and "fosforos" in ingredientes:
                self.papel_sem.release()
            elif "papel" in ingredientes and "fosforos" in ingredientes:
                self.tabaco_sem.release()
            self.mutex.release()
            time.sleep(3)  # Simulamos el tiempo que tarda en colocar los ingredientes

# Función para que el fumador espere a sus ingredientes
def esperar_ingredientes(fumador, ingrediente_sem):
    while True:
        ingrediente_sem.acquire()
        print(f"Agente entrega los ingredientes a Fumador {fumador.nombre}.")
        fumador.fumar()

# Crear instancias del agente y los fumadores
agente = Agente()
fumadortabaco = Fumador("tabaco", "papel", "fuego")
fumadorpapel = Fumador("papel", "tabaco", "fuego")
fumadorfuego = Fumador("fuego", "tabaco", "papel")

# Crear hilos para los fumadores y el agente
with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.submit(esperar_ingredientes, fumadortabaco, agente.tabaco_sem)
    executor.submit(esperar_ingredientes, fumadorpapel, agente.papel_sem)
    executor.submit(esperar_ingredientes, fumadorfuego, agente.fosforos_sem)
    executor.submit(agente.colocar_ingredientes)

    # Mantener el programa en ejecución
    while True:
        pass
