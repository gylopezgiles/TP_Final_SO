import time
import threading
import traceback
import Proceso
import csv

global orden_llegada, sem_db, mutex_cont_lectores, cont_lectores, instante

archivo = ''
orden_llegada = threading.Semaphore()
sem_db = threading.Semaphore()
mutex_cont_lectores = threading.Lock()
cont_lectores = 0
process_in_execution = []
finished_process = []
ready_to_execute = {
    0: [Proceso.Proceso('lector1', 'lector', 0, 2), Proceso.Proceso('lector2', 'lector', 0, 2)],
    1: [Proceso.Proceso('lector3', 'lector', 1, 2)],
    2: [Proceso.Proceso('lector4', 'lector', 2, 2)],
    3: [Proceso.Proceso('escritor1', 'escritor', 3, 4)],
    4: [Proceso.Proceso('lector5', 'lector', 4, 2)],
    5: [Proceso.Proceso('escritor2', 'escritor', 5, 1)]
}
writers = 0
readers = 0


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
    all_process = []
    for time in ready_to_execute:
        all_process.extend(ready_to_execute[time])
    return all_process


def get_finished_process_list():
    finished_process = [Proceso.Proceso('lector1', 'lector', 2, 2),
                        Proceso.Proceso('lector2', 'lector', 2, 5),
                        Proceso.Proceso('escritor1', 'escritor', 3, 4),
                        Proceso.Proceso('lector3', 'lector', 6, 2),
                        Proceso.Proceso('escritor2', 'escritor', 8, 1)]
    return finished_process


def leer_archivo():
    with open(archivo, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            tipo_proceso = row[0]
            tiempo_llegada = row[1]
            tiempo_ejecucion = row[2]
            add_process_to_queue(
                tipo_proceso, tiempo_llegada, tiempo_ejecucion)


def add_process_to_queue(tipo_proceso, tiempo_llegada, tiempo_ejecucion):
    global readers
    global writers
    new_process = Proceso.Proceso(
        '', tipo_proceso, tiempo_llegada, tiempo_ejecucion)
    if new_process.es_lector():
        readers += 1
        new_process.nombre_proceso = 'lector {}'.format(readers)
    if new_process.es_escritor():
        writers += 1
        new_process.nombre_proceso = 'escritor {}'.format(writers)
    ready_to_execute[tiempo_llegada] = ready_to_execute.get(tiempo_llegada, [])
    ready_to_execute[tiempo_llegada].append(new_process)
    analize_start()


def analize_start():
    global readers
    global writers
    if writers == 0 and readers == 1:
        start_simulation()
    if readers == 0 and writers == 1:
        start_simulation()


def load_from_csv():
    ''''''
    # TODO: Carga desde csv


def download_finished_process():
    ''''''
    # TODO: Descargar como csv


def start_simulation():
    ''''''
    # TODO: implementar el try catch aca

# try:
#     # TODO Carga de prueba. Se leerá de un archivo e irá appendeando
#     procesos = [Proceso.Proceso('lector1', 'lector', 2, 2),
#                 Proceso.Proceso('lector2', 'lector', 2, 5),
#                 Proceso.Proceso('escritor1', 'escritor', 3, 4),
#                 Proceso.Proceso('lector3', 'lector', 6, 2),
#                 Proceso.Proceso('escritor2', 'escritor', 8, 1)]
#     max_tiempo_llegada = 8
#
#     rindex = 1
#     windex = 1
#     for i in range(max_tiempo_llegada + 1):
#         print("---------- INSTANTE DE TIEMPO: " + str(i) + " ----------")
#         time.sleep(2)
#         for proceso in procesos:
#             if proceso.tiempo_llegada == i:
#                 if proceso.es_lector():
#                     t = threading.Thread(target=ejecutar_lector, args=(proceso, rindex,))
#                     rindex += 1
#                     t.start()
#                 else:
#                     t = threading.Thread(target=ejecutar_escritor, args=(proceso, windex,))
#                     windex += 1
#                     t.start()
# except:
#     print(str(traceback.format_exc()))
#     print("Error: unable to start thread")

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
