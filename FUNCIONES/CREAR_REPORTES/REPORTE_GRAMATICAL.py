import tkinter as tk
from tkinter import Toplevel, Canvas, Scrollbar
from PIL import Image, ImageTk  #pip install Pillow

def mostrar_gramatical (ventana_principal):
    ventana_imagen = Toplevel(ventana_principal)
    ventana_imagen.title("VISTA REPORTE")
    ventana_imagen.geometry("820x720")
    ventana_imagen.configure(bg="#252950")

     # Label en el centro y en la parte superior
    label_titulo = tk.Label(ventana_imagen, text="REPORTE GRAMATICAL", bg="#252950", fg="white", font=("Arial", 16))
    label_titulo.place(x=300,y=10)
    
    gramatica= tk.Text(ventana_imagen,state='disabled',font=("Helvetica", 12))
    gramatica.configure(bg="#ECEEF1")
    gramatica.place(x=10, y=150, width=800, height=500)

    contenidogram = ""

    with open("gramatica_texto.txt", "r") as archivo:
        gramatica.config(state='normal')
        gramatica.delete(1.0, tk.END) 
        gramatica.insert(tk.END, archivo.read())
        gramatica.config(state='disabled')
    ventana_imagen.mainloop()