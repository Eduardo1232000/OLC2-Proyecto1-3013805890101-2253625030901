from tkinter import messagebox      #MOSTRAR UN MENSAJE AL USUARIO
from tkinter import filedialog      #ABRIR ARCHIVOS
import gramatica
from FUNCIONES.ARBOL.AST import *

def importar_datos():
    archivo_seleccionado = filedialog.askopenfilename(defaultextension=".sql", filetypes=[("Archivos de texto", "*.sql"), ("Todos los archivos", "*.*")])

    if archivo_seleccionado:
        with open(archivo_seleccionado, "r") as archivo:
            contenido = archivo.read()
            respuesta_parser = gramatica.parses(contenido)
            arbol_Temporal = AST(respuesta_parser[0],[],[])
            arbol_Temporal.ejecutar()
            messagebox.showinfo(message="Tablas importadas!", title="Exito")