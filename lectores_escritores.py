import time
import threading
import traceback
import Proceso
import csv

global orden_llegada, sem_db, mutex_cont_lectores, cont_lectores, instante, ready_to_execute

archivo = ''
orden_llegada = threading.Semaphore()
sem_db = threading.Semaphore()
mutex_cont_lectores = threading.Lock()
cont_lectores = 0
ready_to_execute = {}
instante = 0


def ejecutar_lector(proceso, index):
    global cont_lectores
    print("Lector " + str(index) + " esperando para leer")
    orden_llegada.acquire()
    mutex_cont_lectores.acquire()
    if cont_lectores == 0:
        sem_db.acquire()
    cont_lectores += 1
    orden_llegada.release()
    mutex_cont_lectores.release()

    proceso.leer_db(index, instante)
    print("Lector " + str(index) + " terminó de leer")

    mutex_cont_lectores.acquire()
    cont_lectores -= 1
    if cont_lectores == 0:
        sem_db.release()
    mutex_cont_lectores.release()


def ejecutar_escritor(proceso, index):
    print("Escritor " + str(index) + " esperando para escribir")
    orden_llegada.acquire()
    sem_db.acquire()
    orden_llegada.release()

    proceso.escribir_db(index, instante)
    print("Escritor " + str(index) + " terminó de escribir")

    sem_db.release()


def get_process_list():
    global ready_to_execute
    all_process = []
    for time in ready_to_execute:
        all_process.extend(ready_to_execute[time])
    return all_process


def leer_archivo():
    with open(archivo, mode='r') as file:
        reader = csv.reader(file, delimiter=',')
        next(file)
        for row in reader:
            tipo_proceso = row[0]
            tiempo_llegada = row[1]
            tiempo_ejecucion = row[2]
            add_process_to_queue(
                tipo_proceso, tiempo_llegada, tiempo_ejecucion)
            print("tipo proceso: " + tipo_proceso + " tiempo llegada: " +
                  tiempo_llegada + " tiempo ejecucion: " + tiempo_ejecucion)


def add_process_to_queue(tipo_proceso, tiempo_llegada, tiempo_ejecucion):
    global ready_to_execute
    new_process = Proceso.Proceso(tipo_proceso, tiempo_llegada, tiempo_ejecucion)
    ready_to_execute[tiempo_llegada] = ready_to_execute.get(tiempo_llegada, [])
    ready_to_execute[tiempo_llegada].append(new_process)


def analize_start():
    if len(ready_to_execute):
        start_simulation()
    else:
        print("Por el momento no hay procesos para simular")


def load_from_csv():
    global ready_to_execute
    try:
        # TODO: Carga desde csv y ordenamiento de menor a mayor por instante de llegada
        ready_to_execute = {
            2: [Proceso.Proceso('lector', 2, 2), Proceso.Proceso('lector', 2, 5)],
            3: [Proceso.Proceso('escritor', 3, 4)],
            6: [Proceso.Proceso('lector', 6, 2)],
            8: [Proceso.Proceso('escritor', 8, 1)]
        }
        print("Procesos del CSV cargados a la perfección :D\n")
    except:
        print("No se pudo realizar la carga de procesos desde el CSV :(\n")


def download_finished_process():
    ''''''
    # TODO: Descargar como csv


def start_simulation():
    global ready_to_execute
    global instante
    try:
        rindex = 1
        windex = 1
        while instante in range(max(ready_to_execute) + 1) or len(threading.enumerate()) > 1:
            print("---------- INSTANTE DE TIEMPO: " + str(instante) + " ----------")
            time.sleep(1)
            if instante in ready_to_execute:
                for proceso in ready_to_execute[instante]:
                    if proceso.es_lector():
                        t = threading.Thread(target=ejecutar_lector, args=(proceso, rindex,))
                        rindex += 1
                        t.start()
                    else:
                        t = threading.Thread(target=ejecutar_escritor, args=(proceso, windex,))
                        windex += 1
                        t.start()
                    time.sleep(0.15)
            instante += 1
        print("\nSimulación finalizada con éxito :D")
    except:
        print("No se pudo ejecutar la simulación por el siguiente error: \n" + str(traceback.format_exc()))
