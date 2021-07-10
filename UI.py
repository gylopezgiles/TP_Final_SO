import tkinter as tk
from tkinter import font as tkfont
from tkinter import ttk
import lectores_escritores

class ReadersWritersUI(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Simulacion Lectores Escritores")
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, StartSimulation, SeeQueuePage, AddProcessPage, FinishSimulationPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def close_window(self):
        self.destroy()

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def start_without_process(self, page_name):
        self.show_frame(page_name)

    def start_with_process(self, page_name):
        self.show_frame(page_name)

    def add_process(self, process_type, arrival_time, execution_time):
        print(process_type)
        print(arrival_time)
        print(execution_time)
        self.show_frame("StartSimulation")

    def download_final_table(self):
        print("deacargar tabla")

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        button1 = tk.Button(self, text="Empezar simulacion sin procesos precargados",
                            command=lambda: controller.start_without_process("StartSimulation"))
        button2 = tk.Button(self, text="Empezar simulacion con procesos precargados",
                            command=lambda: controller.start_with_process("StartSimulation"))
        button1.pack()
        button2.pack()


class StartSimulation(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        see_button = tk.Button(self, text="Ver cola de planificacion",
                           command=lambda: controller.show_frame("SeeQueuePage"))
        add_button = tk.Button(self, text="Agregar proceso",
                           command=lambda: controller.show_frame("AddProcessPage"))
        finish_button = tk.Button(self, text="Finalizar Simulacion",
                           command=lambda: controller.show_frame("FinishSimulationPage"))
        see_button.pack()
        add_button.pack()
        finish_button.pack()


class SeeQueuePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Cola Planificacion", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        data = lectores_escritores.get_planification_queue()
        tree = ttk.Treeview(self, columns=(1, 2, 3, 4), height=5, show="headings")
        tree.pack()

        tree.heading(1, text="Nombre Proceso")
        tree.heading(2, text="Tipo Proceso")
        tree.heading(3, text="Tiempo Llegada")
        tree.heading(4, text="Tiempo Ejecucion")

        tree.column(1, width=100)
        tree.column(2, width=100)
        tree.column(3, width=100)
        tree.column(4, width=100)

        scroll = ttk.Scrollbar(self, orient="vertical", command=tree.yview)
        scroll.pack(side='right', fill='y')

        tree.configure(yscrollcommand=scroll.set)

        for proceso in data:
            tree.insert('', 'end', values=(proceso.nombre_proceso, proceso.tipo_proceso,
                                           proceso.tiempo_llegada, proceso.tiempo_ejecucion))
        button = tk.Button(self, text="Volver",
                           command=lambda: controller.show_frame("StartSimulation"))
        button.pack()

class AddProcessPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Agregar Proceso", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        tk.Label(self, text="Tipo Proceso:", justify=tk.LEFT, padx=20).pack(anchor=tk.W)
        process_type = tk.StringVar(self, "lector")
        tk.Radiobutton(self, text="Lector", padx=20, variable=process_type, value="lector").pack(anchor=tk.W)
        tk.Radiobutton(self, text="Escritor", padx=20, variable=process_type, value="escritor").pack(anchor=tk.W)
        tk.Label(self, text="Tiempo Llegada").pack(anchor=tk.W)
        arrival_time = tk.IntVar(self, 0)
        tk.Entry(self, textvariable=arrival_time).pack(anchor=tk.CENTER)
        tk.Label(self, text="Tiempo Ejecucion").pack(anchor=tk.W)
        execution_time = tk.IntVar(self, 0)
        tk.Entry(self, textvariable=execution_time).pack(anchor=tk.CENTER)
        save_button = tk.Button(self, text="Guardar",
                           command=lambda: controller.add_process(process_type.get(), arrival_time.get(), execution_time.get()))
        cancel_button = tk.Button(self, text="Cancelar",
                           command=lambda: controller.show_frame("StartSimulation"))
        save_button.pack()
        cancel_button.pack()

class FinishSimulationPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Tabla Final", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        data = lectores_escritores.get_finished_process_list()

        tree = ttk.Treeview(self, columns=(1, 2, 3, 4, 5, 6), height=5, show="headings")
        tree.pack()

        tree.heading(1, text="Nombre Proceso")
        tree.heading(2, text="Tipo Proceso")
        tree.heading(3, text="Tiempo Llegada")
        tree.heading(4, text="Momento Ejecucion")
        tree.heading(5, text="Tiempo Ejecucion")
        tree.heading(6, text="Tiempo Finalizacion")

        tree.column(1, width=100)
        tree.column(2, width=100)
        tree.column(3, width=100)
        tree.column(4, width=100)
        tree.column(5, width=100)
        tree.column(6, width=100)

        scroll = ttk.Scrollbar(self, orient="vertical", command=tree.yview)
        scroll.pack(side='right', fill='y')

        tree.configure(yscrollcommand=scroll.set)

        for proceso in data:
            tree.insert('', 'end', values=(proceso.nombre_proceso, proceso.tipo_proceso, proceso.tiempo_llegada,
                                           proceso.momento_ejecucion, proceso.tiempo_ejecucion, proceso.momento_finalizacion))

        download_button = tk.Button(self, text="Descargar CSV",
                                 command=lambda: controller.download_final_table())
        start_button = tk.Button(self, text="Empezar de nuevo",
                           command=lambda: controller.show_frame("StartPage"))
        close_button = tk.Button(self, text="Salir",
                           command=lambda: controller.close_window())
        start_button.pack()
        close_button.pack()
        download_button.pack()

if __name__ == "__main__":
    app = ReadersWritersUI()
    app.mainloop()