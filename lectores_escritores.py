import threading
import Proceso

orden_llegada = threading.Semaphore()
sem_db = threading.Semaphore()
mutex_cont_lectores = threading.Lock()
cont_lectores = 0

def ejecutar_lector(proceso):
	print("ejecutando ejecutar_lector para proceso: {}".format(proceso.getName()))
	global cont_lectores
	orden_llegada.acquire()
	mutex_cont_lectores.acquire()
	if cont_lectores == 0:
		print('proceso {} bloquea db'.format(proceso.getName()))
		sem_db.acquire()
	cont_lectores += 1
	print('al ejecutar proceso {} contador lectores = {}'.format(proceso.getName(), cont_lectores))
	orden_llegada.release()
	mutex_cont_lectores.release()
	print('proceso {} va a ejecutarse'.format(proceso.getName()))
	proceso.run()
	mutex_cont_lectores.acquire()
	cont_lectores -= 1
	print('luego de ejecutar proceso {} contador lectores = {}'.format(proceso.getName(), cont_lectores))
	if cont_lectores == 0:
		print('proceso {} libera db'.format(proceso.getName()))
		sem_db.release()
	mutex_cont_lectores.release()

def ejecutar_escritor(proceso):
	orden_llegada.acquire()
	print('proceso {} bloquea db'.format(proceso.getName()))
	sem_db.acquire()
	orden_llegada.release()
	print('proceso {} va a ejecutarse'.format(proceso.getName()))
	proceso.run()
	sem_db.release()
	print('proceso {} libera db'.format(proceso.getName()))

lector1 = Proceso.Proceso('lector', 0, 5)
lector1.setName("lector1")
escritor1 = Proceso.Proceso('escritor', 1, 2)
escritor1.setName("escritor1")
lector2 = Proceso.Proceso('lector', 1, 1)
lector2.setName("lector2")
lector3 = Proceso.Proceso('lector', 2, 2)
lector3.setName("lector3")
escritor2 = Proceso.Proceso('escritor', 1, 3)
escritor2.setName("escritor2")
proceso = Proceso.Proceso('proceso', 1, 2)
proceso.setName("proceso")

procesos = [lector1, escritor1, lector2, lector3, escritor2, proceso]

for proceso in procesos:
	if proceso.es_lector():
		print('proceso {} es lector'.format(proceso.getName()))
		ejecutar_lector(proceso)
	else:
		if proceso.es_escritor():
			print('proceso {} es escritor'.format(proceso.getName()))
			ejecutar_escritor(proceso)
		else:
			print('tipo proceso {} no identificado'.format(proceso.tipo_proceso))



