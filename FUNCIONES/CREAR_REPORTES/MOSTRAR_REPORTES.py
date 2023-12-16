import tkinter as tk
from tkinter import Toplevel, Canvas, Scrollbar
from PIL import Image, ImageTk  #pip install Pillow

def mostrar_reporte(ventana_principal,ruta_imagen,titulo):
    ventana_imagen = Toplevel(ventana_principal)
    ventana_imagen.title("VISTA REPORTE")
    ventana_imagen.geometry("720x720")
    ventana_imagen.configure(bg="#252950")

    # Label en el centro y en la parte superior
    label_titulo = tk.Label(ventana_imagen, text=str(titulo), bg="#252950", fg="white", font=("Arial", 16))
    label_titulo.grid(row=0, column=0, sticky="n", pady=(10, 0))

    # Crear un Canvas y agregar barras de desplazamiento
    canvas = Canvas(ventana_imagen, bg="#252950", highlightthickness=0)
    scrollbar_y = Scrollbar(ventana_imagen, orient="vertical", command=canvas.yview)
    scrollbar_x = Scrollbar(ventana_imagen, orient="horizontal", command=canvas.xview)
    canvas.config(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

    # Cargar la imagen y mostrarla en el Canvas
    imagen_pil = Image.open(ruta_imagen)
    imagen_tk = ImageTk.PhotoImage(imagen_pil)

    canvas.create_image(0, 0, anchor="nw", image=imagen_tk)

    # Empacar el Canvas y las barras de desplazamiento utilizando grid
    canvas.grid(row=1, column=0, sticky="nsew", pady=(10, 0))
    scrollbar_y.grid(row=1, column=1, sticky="ns")
    scrollbar_x.grid(row=2, column=0, sticky="ew", pady=(0, 20))  # Configurar el ancho y la posición

    # Configurar el área de desplazamiento del Canvas
    canvas.config(scrollregion=canvas.bbox("all"))

    # Configurar el estiramiento de las columnas y filas
    ventana_imagen.grid_rowconfigure(1, weight=1)
    ventana_imagen.grid_columnconfigure(0, weight=1)

    ventana_imagen.mainloop()