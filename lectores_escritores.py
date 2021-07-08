import time
import threading
import Proceso

orden_llegada = threading.Semaphore()
sem_db = threading.Semaphore()
mutex_cont_lectores = threading.Lock()
cont_lectores = 0

def ejecutar_lector(proceso):
	orden_llegada.acquire()
	mutex_cont_lectores.acquire()
	if cont_lectores == 0:
		sem_db.acquire()
	cont_lectores += 1
	orden_llegada.release()
	mutex_cont_lectores.release()
	proceso.leer_db()
	mutex_cont_lectores.acquire()
	cont_lectores -= 1
	if cont_lectores == 0:
		sem_db.release()
	mutex_cont_lectores.release()

def ejecutar_escritor(proceso):
	orden_llegada.acquire()
	sem_db.acquire()
	orden_llegada.release()
	proceso.escribir_db()
	sem_db.release()

lector1 = Proceso.Proceso('lector', 0, 5)
escritor1 = Proceso.Proceso('escritor', 1, 2)
lector2 = Proceso.Proceso('lector', 1, 1)
lector3 = Proceso.Proceso('lector', 2, 2)
escritor2 = Proceso.Proceso('escritor', 1, 3)

procesos = []
procesos.append(lector1)
procesos.append(escritor1)
procesos.append(lector2)
procesos.append(lector3)
procesos.append(escritor2)
for proceso in procesos:

