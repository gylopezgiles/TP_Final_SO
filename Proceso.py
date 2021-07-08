import time
import threading

class Proceso(threading.Thread):

	def __init__(self, tipo_proceso, tiempo_llegada, tiempo_ejecucion):
		threading.Thread.__init__(self)
		self.tipo_proceso = tipo_proceso
		self.tiempo_llegada = tiempo_llegada
		self.tiempo_ejecucion = tiempo_ejecucion

	def run(self):
		if self.es_lector():
			print('proceso {} va a leer db'.format(self.getName()))
			self.leer_db()
		if self.es_escritor():
			print('proceso {} va a escribir db'.format(self.getName()))
			self.escribir_db()

	def leer_db(self):
		time.sleep(self.tiempo_ejecucion)

	def escribir_db(self):
		time.sleep(self.tiempo_ejecucion)

	def es_lector(self):
		return self.tipo_proceso.lower() == "lector"

	def es_escritor(self):
		return self.tipo_proceso.lower() == "escritor"
