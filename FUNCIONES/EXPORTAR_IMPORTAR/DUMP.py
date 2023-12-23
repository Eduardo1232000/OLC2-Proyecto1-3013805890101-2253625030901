import os
import tkinter as tk
import xml.etree.ElementTree as ET
from tkinter import messagebox      #MOSTRAR UN MENSAJE AL USUARIO

def mostrar_bases_dump(ventana_principal):
    ventana_archivos = tk.Toplevel(ventana_principal)
    ventana_archivos.title("Bases de Datos")
    ventana_archivos.geometry("480x320")
    ventana_archivos.configure(bg="#1A1C2F")

    label_titulo = tk.Label(ventana_archivos, text="Selecciona una base de datos",bg="#1A1C2F", fg="white", font=("Helvetica", 18))
    label_titulo.place(x=50,y=10,width=380,height=60)
    # Crear la lista de archivos
    lista_archivos = tk.Listbox(ventana_archivos, selectmode=tk.SINGLE)
    lista_archivos.place(x=20,y=70,width=440,height=200)
    # Cargar automáticamente los archivos de la carpeta al iniciar
    cargar_archivos_dump(lista_archivos)

    # Botón para obtener la selección
    boton_seleccionar = tk.Button(ventana_archivos, text="Cancelar", command=lambda:cancelar_dump(ventana_archivos),bg="#A90F0F", fg="white", font=("Helvetica", 14))
    boton_seleccionar.place(x=60,y=280,width=150,height=30) 

    boton_seleccionar = tk.Button(ventana_archivos, text="Confirmar", command=lambda: obtener_seleccion_dump(ventana_principal,ventana_archivos,lista_archivos),bg="#0FA926", fg="white", font=("Helvetica", 14))
    boton_seleccionar.place(x=270,y=280,width=150,height=30) 

def cancelar_dump(ventana_actual):
    ventana_actual.destroy()

def atras_dump(ventana_principal,ventana_actual):
    mostrar_bases_dump(ventana_principal)
    ventana_actual.destroy()

def cargar_archivos_dump(lista_archivos):
    # Limpia la lista actual
    lista_archivos.delete(0, tk.END)

    # Obtiene la lista de archivos en la carpeta
    archivos_en_carpeta = [archivo for archivo in os.listdir("BASE_DATOS/") if archivo.endswith(".xml")]

    # Agrega los nombres de los archivos a la lista
    for archivo in archivos_en_carpeta:
        lista_archivos.insert(tk.END, archivo)

def obtener_seleccion_dump(ventana_principal,ventana_archivos,lista_archivos):
    # Obtiene el índice seleccionado en la lista
    indice_seleccionado = lista_archivos.curselection()

    if indice_seleccionado:
        archivo_seleccionado = lista_archivos.get(indice_seleccionado[0])
        print(f"Archivo seleccionado: {archivo_seleccionado}")
        mostrar_tablas_dump(ventana_principal,archivo_seleccionado)
        ventana_archivos.destroy()

def mostrar_tablas_dump(ventana_principal,nombre_base):
    #OBTENER LISTA DE NOMBRES DE TABLAS
    lista_nombre_tablas = []
    ruta = "BASE_DATOS/"+str(nombre_base)
    tree = ET.parse(ruta)
    root = tree.getroot()
    base_existente = None
    for base in root.findall('base'):
        for tabla in base.findall('tabla'):
            #print(tabla.attrib['name'])
            lista_nombre_tablas.append(tabla.attrib['name'])

    ventana_tablas = tk.Toplevel(ventana_principal)
    ventana_tablas.title("Selecciona las Tablas")
    ventana_tablas.geometry("480x320")
    ventana_tablas.configure(bg="#1A1C2F")

    label_titulo = tk.Label(ventana_tablas, text="Selecciona una o mas Tablas",bg="#1A1C2F", fg="white", font=("Helvetica", 18))
    label_titulo.place(x=50,y=10,width=380,height=60)

    # Crear la lista de archivos
    lista_tablas = tk.Listbox(ventana_tablas)
    lista_tablas.place(x=20,y=70,width=440,height=200)
    # Cargar automáticamente los archivos de la carpeta al iniciar
    cargar_tablas_dump(lista_tablas,lista_nombre_tablas)

    boton_seleccionar = tk.Button(ventana_tablas, text="Cancelar", command=lambda:cancelar_dump(ventana_tablas),bg="#A90F0F", fg="white", font=("Helvetica", 14))
    boton_seleccionar.place(x=37,y=280,width=110,height=30) 

    boton_seleccionar = tk.Button(ventana_tablas, text="Atras", command=lambda:atras_dump(ventana_principal,ventana_tablas),bg="#A9A90F", fg="white", font=("Helvetica", 14))
    boton_seleccionar.place(x=185,y=280,width=110,height=30) 

    boton_seleccionar = tk.Button(ventana_tablas, text="Confirmar", command=lambda: obtener_seleccion_tablas_dump(ventana_principal,ventana_tablas,lista_tablas,nombre_base),bg="#0FA926", fg="white", font=("Helvetica", 14))
    boton_seleccionar.place(x=330,y=280,width=110,height=30) 

def cargar_tablas_dump(lista_tablas,lista_nombres):
    # Limpia la lista actual
    lista_tablas.delete(0, tk.END)

    # Agrega los nombres de los archivos a la lista
    for archivo in lista_nombres:
        lista_tablas.insert(tk.END, archivo)

def obtener_seleccion_tablas_dump(ventana_principal,ventana_tablas,lista_tablas,nombre_base):
    #print(nombre_base)
    ruta = "BASE_DATOS/"+str(nombre_base)
    tree = ET.parse(ruta)
    root = tree.getroot()

    base_existente = None
    contenido_archivo = "CREATE DATA BASE "+str(nombre_base[:-4])+";\n\n"
    contenido_archivo += "USE "+str(nombre_base[:-4])+";\n\n"
    comando = ""

    for base in root.findall('base'):
        #RECORRER TABLAS
        contenido = ""
        for tabla in base.findall('tabla'):
            nombre_tabla = tabla.attrib["name"]
            comando = "CREATE TABLE "+str(nombre_tabla)+" (\n"

            contador = 0
            for campos in tabla.findall('campo'):
                if(contador !=0):                                                           #NOMBRE
                    comando +=",\n"
                comando += str(campos[0].text) + " "
                
                if(campos[1].text == "NVARCHAR" or campos[1].text == "NCHAR"):              #TIPO
                    comando += campos[1].text + "(" + str(campos[1].attrib['size']) +") "
                else:
                    comando += campos[1].text +" "
                
                if(campos[2].text == "true"):                                               #NULO
                    comando += "NULL "
                else:
                    comando += "NOT NULL "

                if(campos[3].text == "true"):                                               #PRIMARY KEY
                    comando += "PRIMARY KEY "

                if(campos[4].text !="false" and campos[5].text != "false"):                 #FOREIGN KEY
                    comando += "REFERENCE "+str(campos[4].text) +"("+ str(campos[5].text)+")"

                contador += 1

            #print(comando)
            comando +="\n);"
            contenido_archivo += comando +"\n\n"

        for funciones in base.findall('funcion'):
            nombre_funcion = funciones.attrib['name']
            comando = "CREATE FUNCTION "+str(nombre_funcion) 
            for parametros in funciones.findall('parameters'):
                comando += "("
                contador = 0
                for param in parametros:
                    if(contador !=0):
                        comando += ", "
                    comando += "@"+str(param.attrib['name']) +" "
                    if(param.attrib['type'] =="NVARCHAR" or param.attrib['type'] == "NCHAR"):
                        comando += param.attrib['type'] + "("+param.attrib['size']+")"
                    else:
                        comando += param.attrib['type']
                    contador +=1
                comando+=")"
            for retu in funciones.findall('retorno'):
                comando += "\nRETURN "
                if(retu.attrib['type'] == "NVARCHAR"or retu.attrib['type']== "NCHAR"):
                    comando += str(retu.attrib['type']) +"("+ str(retu.attrib['size']) +")"
                else:
                    comando += str(retu.attrib['type']) 
            comando += "\nAS\nBEGIN"

            for sentencias in  funciones.findall('sentencias'):
                for sent in sentencias:
                    comando += "\n\t"+str(sent.text)
            comando += "\n\nEND;"

            contenido_archivo += comando
            contenido_archivo +="\n\n"

        for procedures in  base.findall('procedure'):
            nombre_funcion = procedures.attrib['name']
            comando = "CREATE PROCEDURE "+str(nombre_funcion) 
            for parametros in procedures.findall('parameters'):
                comando += "("
                contador = 0
                for param in parametros:
                    if(contador !=0):
                        comando += ", "
                    comando += "@"+str(param.attrib['name']) +" "
                    if(param.attrib['type'] =="NVARCHAR" or param.attrib['type'] == "NCHAR"):
                        comando += param.attrib['type'] + "("+param.attrib['size']+")"
                    else:
                        comando += param.attrib['type']
                    contador +=1
                comando+=")"
            comando += "\nAS\nBEGIN"

            for sentencias in  procedures.findall('sentencias'):
                for sent in sentencias:
                    comando += "\n\t"+str(sent.text)
            comando += "\n\nEND;"

            contenido_archivo += comando 
            contenido_archivo +="\n\n"  
            
    with open("DUMPS/"+str(nombre_base[:-4])+".sql", "w") as archivo:
        archivo.write(contenido_archivo)  
        archivo.close()
    ventana_tablas.destroy()
    messagebox.showinfo(message="Tablas exportadas!", title="Exito")