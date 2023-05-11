import concurrent.futures
import random
import time
import threading
import tkinter as tk

# Clase Fumador
class Fumador:
    def __init__(self, nombre, ingrediente1, ingrediente2):
        self.nombre = nombre
        self.ingrediente1 = ingrediente1
        self.ingrediente2 = ingrediente2
        self.estado = "Esperando"

    def fumar(self):
        self.estado = "Fumando"
        time.sleep(2)  # Simulamos el tiempo que tarda en fumar
        self.estado = "Enmonado"

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
        fumador.estado = "Recibiendo ingredientes"
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

    # Interfaz gráfica
    root = tk.Tk()
    root.title("Fumadores")
    root.geometry("300x150")

    # Etiquetas de estado de los fumadores
    label1 = tk.Label(root, text="Fumador tabaco: Esperando", fg="black")
    label1.pack()
    label2 = tk.Label(root, text="Fumador papel: Esperando", fg="black")
    label2.pack()
    label3 = tk.Label(root, text="Fumador fuego: Esperando", fg="black")
    label3.pack()

    def actualizar_interfaz():
        label1.config(text=f"Fumador tabaco: {fumadortabaco.estado}", fg=get_color(fumadortabaco.estado))
        label2.config(text=f"Fumador papel: {fumadorpapel.estado}", fg=get_color(fumadorpapel.estado))
        label3.config(text=f"Fumador fuego: {fumadorfuego.estado}", fg=get_color(fumadorfuego.estado))
        root.after(1000, actualizar_interfaz)

    def get_color(estado):
        if estado == "Esperando":
            return "black"
        elif estado == "Recibiendo ingredientes":
            return "blue"
        elif estado == "Fumando":
            return "green"
        elif estado == "Enmonado":
            return "red"

    # Iniciar actualización de la interfaz
    actualizar_interfaz()

    # Ejecutar la interfaz gráfica
    root.mainloop()

