import time
import threading
import traceback
import Proceso

global orden_llegada, sem_db, mutex_cont_lectores, cont_lectores, instante

orden_llegada = threading.Semaphore()
sem_db = threading.Semaphore()
mutex_cont_lectores = threading.Lock()
cont_lectores = 0


def ejecutar_lector(proceso, i):
    global cont_lectores
    print("Lector " + str(i) + " esperando para leer")
    orden_llegada.acquire()
    mutex_cont_lectores.acquire()
    if cont_lectores == 0:
        sem_db.acquire()
    cont_lectores += 1
    orden_llegada.release()
    mutex_cont_lectores.release()

    proceso.leer_db(i)
    print("Lector " + str(i) + " terminó de leer")

    mutex_cont_lectores.acquire()
    cont_lectores -= 1
    if cont_lectores == 0:
        sem_db.release()
    mutex_cont_lectores.release()


def ejecutar_escritor(proceso, i):
    print("Escritor " + str(i) + " esperando para escribir")
    orden_llegada.acquire()
    sem_db.acquire()
    orden_llegada.release()

    proceso.escribir_db(i)
    print("Escritor " + str(i) + " terminó de escribir")

    sem_db.release()

def get_planification_queue():
    procesos = [Proceso.Proceso('lector1', 'lector', 2, 2),
                Proceso.Proceso('lector2', 'lector', 2, 5),
                Proceso.Proceso('escritor1', 'escritor', 3, 4),
                Proceso.Proceso('lector3', 'lector', 6, 2),
                Proceso.Proceso('escritor2', 'escritor', 8, 1)]
    return procesos

def get_finished_process_list():
    procesos = [Proceso.Proceso('lector1', 'lector', 2, 2),
                Proceso.Proceso('lector2', 'lector', 2, 5),
                Proceso.Proceso('escritor1', 'escritor', 3, 4),
                Proceso.Proceso('lector3', 'lector', 6, 2),
                Proceso.Proceso('escritor2', 'escritor', 8, 1)]
    return procesos


try:
    # TODO Carga de prueba. Se leerá de un archivo e irá appendeando
    procesos = [Proceso.Proceso('lector1', 'lector', 2, 2),
                Proceso.Proceso('lector2', 'lector', 2, 5),
                Proceso.Proceso('escritor1', 'escritor', 3, 4),
                Proceso.Proceso('lector3', 'lector', 6, 2),
                Proceso.Proceso('escritor2', 'escritor', 8, 1)]
    max_tiempo_llegada = 8

    rindex = 1
    windex = 1
    for i in range(max_tiempo_llegada + 1):
        print("---------- INSTANTE DE TIEMPO: " + str(i) + " ----------")
        time.sleep(2)
        for proceso in procesos:
            if proceso.tiempo_llegada == i:
                if proceso.es_lector():
                    t = threading.Thread(target=ejecutar_lector, args=(proceso, rindex,))
                    rindex += 1
                    t.start()
                else:
                    t = threading.Thread(target=ejecutar_escritor, args=(proceso, windex,))
                    windex += 1
                    t.start()
except:
    print(str(traceback.format_exc()))
    print("Error: unable to start thread")

# lector1 = Proceso.Proceso('lector', 0, 5)
# escritor1 = Proceso.Proceso('escritor', 1, 2)
# lector2 = Proceso.Proceso('lector', 1, 1)
# lector3 = Proceso.Proceso('lector', 2, 2)
# escritor2 = Proceso.Proceso('escritor', 1, 3)
#
# procesos = []
# procesos.append(lector1)
# procesos.append(escritor1)
# procesos.append(lector2)
# procesos.append(lector3)
# procesos.append(escritor2)
# for proceso in procesos:
