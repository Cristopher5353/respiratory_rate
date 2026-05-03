import tkinter as tk
from tkinter import ttk, messagebox
import serial
import threading
import time
import matplotlib.pyplot as plt
from collections import deque

PUERTO = "COM4"

arduino = None
nivel = 0.0

pacientes = [
    {"nombre": "Juan", "paterno": "Perez", "materno": "Lopez", "edad": 25, "rpm": "-", "estado": "-"},
    {"nombre": "Maria", "paterno": "Gomez", "materno": "Rojas", "edad": 30, "rpm": "-", "estado": "-"},
    {"nombre": "Carlos", "paterno": "Torres", "materno": "Diaz", "edad": 22, "rpm": "-", "estado": "-"},
    {"nombre": "Ana", "paterno": "Vargas", "materno": "Soto", "edad": 28, "rpm": "-", "estado": "-"}
]

paciente_index = None

def reiniciar_arduino():
    global arduino
    try:
        if arduino:
            arduino.close()

        arduino = serial.Serial(PUERTO, 9600)
        arduino.timeout = 0.05
        time.sleep(2)

    except Exception as e:
        messagebox.showerror("Error", str(e))


# GUI
root = tk.Tk()
root.title("Monitoreo Respiratorio")

columns = ("Nombre", "Paterno", "Materno", "Edad", "RPM", "Estado")
tree = ttk.Treeview(root, columns=columns, show="headings")

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=100)

tree.pack()

for p in pacientes:
    tree.insert("", tk.END, values=(
        p["nombre"], p["paterno"], p["materno"],
        p["edad"], p["rpm"], p["estado"]
    ))

def seleccionar(event):
    global paciente_index
    selected = tree.selection()
    if selected:
        paciente_index = tree.index(selected[0])

tree.bind("<<TreeviewSelect>>", seleccionar)

def deseleccionar():
    global paciente_index
    tree.selection_remove(tree.selection())
    paciente_index = None

# MEDICIÓN + GRÁFICA
def medir_y_graficar():
    global paciente_index, arduino, nivel

    reiniciar_arduino()

    data = deque([0.0]*80, maxlen=80)
    nivel = 0.0

    plt.ion()
    fig, ax = plt.subplots()
    line, = ax.plot(list(data))

    ax.set_title("Frecuencia Respiratoria (Tiempo Real)")
    ax.set_ylim(0, 1.2)

    while True:
        linea = arduino.readline().decode(errors='ignore').strip()

        if linea and "RESP" in linea:
            nivel = 1.0
        else:
            nivel *= 0.92

        data.append(nivel)

        line.set_ydata(list(data))
        line.set_xdata(range(len(data)))

        ax.relim()
        ax.autoscale_view()

        fig.canvas.draw()
        fig.canvas.flush_events()

        if linea.startswith("RPM:"):
            try:
                partes = linea.split(",")

                rpm = int(partes[0].split(":")[1])
                estado = partes[1].split(":")[1]

                if paciente_index is not None:
                    pacientes[paciente_index]["rpm"] = rpm
                    pacientes[paciente_index]["estado"] = estado

                    item = tree.get_children()[paciente_index]
                    tree.item(item, values=(
                        pacientes[paciente_index]["nombre"],
                        pacientes[paciente_index]["paterno"],
                        pacientes[paciente_index]["materno"],
                        pacientes[paciente_index]["edad"],
                        rpm,
                        estado
                    ))

                    messagebox.showinfo("Resultado", f"RPM: {rpm} - {estado}")

                break

            except:
                print("Error procesando")

    plt.close(fig)

def iniciar_medicion():
    if paciente_index is None:
        messagebox.showwarning("Aviso", "Seleccione un paciente")
        return

    hilo = threading.Thread(target=medir_y_graficar)
    hilo.start()

btn_start = tk.Button(root, text="Iniciar Medición", command=iniciar_medicion)
btn_start.pack()

btn_deselect = tk.Button(root, text="Deseleccionar", command=deseleccionar)
btn_deselect.pack()

root.mainloop()