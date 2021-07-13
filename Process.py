import time
import threading


class Process(threading.Thread):

    def __init__(self, process_type, arrival_time, execution_time):
        super().__init__()
        self.process_type = process_type
        self.arrival_time = arrival_time
        self.execution_time = execution_time
        self.execution_instant = 0
        self.end_instant = 0

    def run(self):
        time.sleep(self.execution_time)

    def read_db(self, i, instant):
        self.execution_instant = instant
        self.end_instant = instant + self.execution_time
        t = 0
        while t < self.execution_time:
            print("Lector " + str(i) + " está leyendo datos en la base")
            time.sleep(1)
            t += 1

    def write_db(self, i, instant):
        self.execution_instant = instant
        self.end_instant = instant + self.execution_time
        t = 0
        while t < self.execution_time:
            print("Escritor " + str(i) + " está escribiendo datos en la base")
            time.sleep(1)
            t += 1

    def is_reader(self):
        return self.process_type.lower() == "lector"

    def is_writer(self):
        return self.process_type.lower() == "escritor"
