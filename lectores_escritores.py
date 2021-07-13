import time
import threading
import traceback
import Process
import csv

global arrival_order, sem_db, mutex_count_readers, count_readers, instant, ready_to_execute

process_file = 'procesos.csv'
finished_process_file = 'procesos_finalizados.csv'
arrival_order = threading.Semaphore()
sem_db = threading.Semaphore()
mutex_count_readers = threading.Lock()
count_readers = 0
ready_to_execute = {}
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

    process.write_db(index, instant)
    print("Escritor " + str(index) + " terminó de escribir")

    sem_db.release()


def get_process_list():
    global ready_to_execute
    all_process = []
    for moment in ready_to_execute:
        all_process.extend(ready_to_execute[moment])
    return all_process


def add_process_to_queue(process_type, arrival_time, execution_time):
    global ready_to_execute
    new_process = Process.Process(process_type, arrival_time, execution_time)
    ready_to_execute[arrival_time] = ready_to_execute.get(arrival_time, [])
    ready_to_execute[arrival_time].append(new_process)


def analyze_start():
    if len(ready_to_execute):
        start_simulation()
    else:
        print("Por el momento no hay procesos para simular")


def load_from_csv():
    global ready_to_execute
    try:
        with open(process_file) as file:
            reader = csv.reader(file, delimiter=',')
            for process_type, arrival_time, execution_time in reader:
                add_process_to_queue(process_type, int(arrival_time), int(execution_time))
                print("tipo proceso: " + process_type + " tiempo llegada: " +
                      arrival_time + " tiempo ejecucion: " + execution_time)
        print("Procesos del CSV cargados a la perfección :D\n")
    except:
        print("No se pudo realizar la carga de procesos desde el CSV :(\n")


def download_finished_process():
    try:
        with open(finished_process_file, "a") as archivo:
            archivo.write('tipo_proceso, tiempo_llegada, momento_ejecucion, '
                          'tiempo_ejecucion, tiempo_finalizacion\n')
            finished_process = get_process_list()
            for process in finished_process:
                archivo.write('{}, {}, {}, {}, {}\n'.format(process.process_type, process.arrival_time, process.execution_instant,
                                                            process.execution_time, process.end_instant))
    except IOError:
        print('Archivo {} inválido, no puede abrirse.'.format(finished_process_file))


def start_simulation():
    global ready_to_execute
    global instant
    try:
        rindex = 1
        windex = 1
        while instant in range(max(ready_to_execute) + 1) or len(threading.enumerate()) > 1:
            print("---------- INSTANTE DE TIEMPO: " + str(instant) + " ----------")
            #print("cola de listos:")
            #for process in get_process_list():
                #print('tipo proceso: {} tiempo llegada: {} tiempo ejecucion: {}'.format(process.tipo_proceso, process.tiempo_llegada, process.tiempo_ejecucion))
            time.sleep(1)
            if instant in ready_to_execute:
                for process in ready_to_execute[instant]:
                    if process.is_reader():
                        t = threading.Thread(target=run_reader, args=(process, rindex,))
                        rindex += 1
                        t.start()
                    else:
                        t = threading.Thread(target=run_writer, args=(process, windex,))
                        windex += 1
                        t.start()
                    time.sleep(0.15)
            instant += 1
        print("\nSimulación finalizada con éxito :D")
    except:
        print("No se pudo ejecutar la simulación por el siguiente error: \n" + str(traceback.format_exc()))
