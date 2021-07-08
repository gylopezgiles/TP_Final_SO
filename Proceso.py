import time
import threading

class Proceso(threading.Thread):

	def __init__(self, tipo_proceso, tiempo_llegada, tiempo_ejecucion):
		self.tipo_proceso = tipo_proceso
		self.tiempo_llegada = tiempo_llegada
		self.tiempo_ejecucion = tiempo_ejecucion

	def run(self):
		time.sleep(self.tiempo_ejecucion)

	def leer_db(self):
		time.sleep(self.tiempo_ejecucion)

	def escribir_db(self):
		time.sleep(self.tiempo_ejecucion)

	def es_lector(self):
		return self.tipo_proceso.lower() == "lector"

	def es_escritor(self):
		return self.tipo_proceso.lower() == "escritor"
