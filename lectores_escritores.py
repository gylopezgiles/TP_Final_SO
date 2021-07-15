import time
import threading
import traceback
import Process
import csv
import sys
# import tkinter as tk
from tkinter import filedialog as fd

global arrival_order, sem_db, mutex_count_readers, count_readers, instant, ready_to_execute, ready_queue

finished_process_file = 'procesos_finalizados.csv'
arrival_order = threading.Semaphore()
sem_db = threading.Semaphore()
mutex_count_readers = threading.Lock()
count_readers = 0
ready_to_execute = {}
ready_queue = []
instant = 0


def run_reader(process, index):
    global count_readers
    print("Lector " + str(index) + " esperando para leer")
    arrival_order.acquire()
    mutex_count_readers.acquire()
    if count_readers == 0:
        sem_db.acquire()
    count_readers += 1
    arrival_order.release()
    mutex_count_readers.release()

    ready_queue.pop(0)
    process.read_db(index, instant)
    print("Lector " + str(index) + " terminó de leer")

    mutex_count_readers.acquire()
    count_readers -= 1
    if count_readers == 0:
        sem_db.release()
    mutex_count_readers.release()


def run_writer(process, index):
    print("Escritor " + str(index) + " esperando para escribir")
    arrival_order.acquire()
    sem_db.acquire()
    arrival_order.release()

    ready_queue.pop(0)
    process.write_db(index, instant)
    print("Escritor " + str(index) + " terminó de escribir")

    sem_db.release()


def initialize():
    global ready_to_execute, instant, ready_queue
    ready_to_execute = {}
    ready_queue = []
    instant = 0


def get_process_list():
    global ready_to_execute
    all_process = []
    for moment in ready_to_execute:
        all_process.extend(ready_to_execute[moment])
    return all_process


def add_process_to_queue(process_type, arrival_time, execution_time):
    global ready_to_execute, instant
    # Se reinicia instante por si se quiere simular otra vez con el nuevo proceso agregado
    instant = 0
    new_process = Process.Process(process_type, arrival_time, execution_time)
    ready_to_execute[arrival_time] = ready_to_execute.get(arrival_time, [])
    ready_to_execute[arrival_time].append(new_process)
    # Ordena de menor a mayor por tiempo de llegada
    ready_to_execute = dict(sorted(ready_to_execute.items(), key=lambda item: item[0]))


def analyze_start():
    if len(ready_to_execute):
        start_simulation()
    else:
        print("Por el momento no hay procesos para simular")


def load_from_csv():
    global ready_to_execute
    try:
        # tk.Tk().withdraw()
        # El archivo CSV a adjuntar debe tener el mismo formato que procesos_ejemplo.csv
        process_file = fd.askopenfilename(title="Select file", filetypes=(("CSV Files", "*.csv"),))
        if process_file:
            with open(process_file) as file:
                reader = csv.reader(file, delimiter=',')
                if len(next(reader)) != 3:
                    raise ValueError("La cantidad de columnas debe ser 3")
                for process_type, arrival_time, execution_time in reader:
                    print("CARGANDO tipo proceso: " + process_type + " tiempo llegada: " +
                          arrival_time + " tiempo ejecucion: " + execution_time)
                    if process_type.lower() != "lector" and process_type.lower() != "escritor":
                        raise ValueError("Los valores del tipo de proceso solo pueden ser 'escritor' o 'lector'")
                    if not arrival_time.isdigit() or not execution_time.isdigit() or execution_time == '0':
                        raise ValueError("Los valores del tiempo de llegada y ejecución deben ser números naturales ("
                                         "incluído el 0 para el caso de llegada)")
                    add_process_to_queue(process_type, int(arrival_time), int(execution_time))
            print("Procesos del CSV cargados a la perfección :D\n")
        else:
            raise IOError("No se cargó ningun archivo CSV")
    except ValueError as ve:
        print("No se pudo cargar el CSV completamente por el siguiente motivo: \n" + str(ve))
    except IOError as io:
        print("No se pudo cargar el CSV completamente por el siguiente motivo: \n" + str(io))
    except Exception:
        print("No se pudo cargar el CSV completamente por el siguiente motivo: \n" + str(traceback.format_exc()))


def download_finished_process():
    try:
        with open(finished_process_file, "a") as archivo:
            archivo.write('tipo_proceso, tiempo_llegada, momento_ejecucion, '
                          'tiempo_ejecucion, tiempo_finalizacion\n')
            finished_process = get_process_list()
            for process in finished_process:
                archivo.write(
                    '{}, {}, {}, {}, {}\n'.format(process.process_type, process.arrival_time, process.execution_instant,
                                                  process.execution_time, process.end_instant))
    except IOError:
        print('Archivo {} inválido, no puede abrirse.'.format(finished_process_file))


def start_simulation():
    global ready_to_execute
    global instant
    global ready_queue
    try:
        rindex = 1
        windex = 1
        while instant in range(max(ready_to_execute) + 1) or len(threading.enumerate()) > 1:
            print("---------- INSTANTE DE TIEMPO: " + str(instant) + " ----------")
            time.sleep(1)
            if instant in ready_to_execute:
                for process in ready_to_execute[instant]:
                    if process.is_reader():
                        ready_queue.append("Lector " + str(rindex))
                        t = threading.Thread(target=run_reader, args=(process, rindex,))
                        t.daemon = True
                        rindex += 1
                        t.start()
                    else:
                        ready_queue.append("Escritor " + str(windex))
                        t = threading.Thread(target=run_writer, args=(process, windex,))
                        t.daemon = True
                        windex += 1
                        t.start()
                    time.sleep(0.15)
            print("Cola de listos: ")
            print(ready_queue)
            instant += 1
        print("\nSimulación finalizada con éxito :D")
    except KeyboardInterrupt:
        print("Simulación interrumpida")
        sys.exit(0)
    except Exception:
        print("No se pudo ejecutar la simulación por el siguiente error: \n" + str(traceback.format_exc()))
