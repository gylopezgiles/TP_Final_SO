import time
import threading


class Proceso(threading.Thread):

    def __init__(self, tipo_proceso, tiempo_llegada, tiempo_ejecucion):
        super().__init__()
        # self.nombre_proceso = nombre_proceso
        self.tipo_proceso = tipo_proceso
        self.tiempo_llegada = tiempo_llegada
        self.tiempo_ejecucion = tiempo_ejecucion
        self.momento_ejecucion = 0
        self.momento_finalizacion = 0

    def run(self):
        time.sleep(self.tiempo_ejecucion)

    def leer_db(self, i, instante):
        self.momento_ejecucion = instante
        self.momento_finalizacion = instante + self.tiempo_ejecucion
        t = 0
        while t < self.tiempo_ejecucion:
            print("Lector " + str(i) + " está leyendo datos en la base")
            time.sleep(1)
            t += 1

    def escribir_db(self, i, instante):
        self.momento_ejecucion = instante
        self.momento_finalizacion = instante + self.tiempo_ejecucion
        t = 0
        while t < self.tiempo_ejecucion:
            print("Escritor " + str(i) + " está escribiendo datos en la base")
            time.sleep(1)
            t += 1

    def es_lector(self):
        return self.tipo_proceso.lower() == "lector"

    def es_escritor(self):
        return self.tipo_proceso.lower() == "escritor"
