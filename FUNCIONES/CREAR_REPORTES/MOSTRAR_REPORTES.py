import tkinter as tk
from tkinter import Toplevel
from PIL import Image, ImageTk  #pip install Pillow

def mostrar_reporte(ventana_principal,ruta_imagen):
    ventana_imagen = Toplevel(ventana_principal)
    imagen_pil = Image.open(ruta_imagen)
    imagen_tk = ImageTk.PhotoImage(imagen_pil)

    etiqueta_imagen = tk.Label(ventana_imagen, image=imagen_tk)
    etiqueta_imagen.image = imagen_tk  
    etiqueta_imagen.pack()