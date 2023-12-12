import os
import tkinter as tk
import xml.etree.ElementTree as ET
from tkinter import messagebox      #MOSTRAR UN MENSAJE AL USUARIO

def mostrar_bases(ventana_principal):
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
    cargar_archivos(lista_archivos)

    # Botón para obtener la selección
    boton_seleccionar = tk.Button(ventana_archivos, text="Cancelar", command=lambda:cancelar(ventana_archivos),bg="#A90F0F", fg="white", font=("Helvetica", 14))
    boton_seleccionar.place(x=60,y=280,width=150,height=30) 

    boton_seleccionar = tk.Button(ventana_archivos, text="Confirmar", command=lambda: obtener_seleccion(ventana_principal,ventana_archivos,lista_archivos),bg="#0FA926", fg="white", font=("Helvetica", 14))
    boton_seleccionar.place(x=270,y=280,width=150,height=30) 

def cancelar(ventana_actual):
    ventana_actual.destroy()

def atras(ventana_principal,ventana_actual):
    mostrar_bases(ventana_principal)
    ventana_actual.destroy()

def cargar_archivos(lista_archivos):
    # Limpia la lista actual
    lista_archivos.delete(0, tk.END)

    # Obtiene la lista de archivos en la carpeta
    archivos_en_carpeta = [archivo for archivo in os.listdir("BASE_DATOS/") if archivo.endswith(".xml")]

    # Agrega los nombres de los archivos a la lista
    for archivo in archivos_en_carpeta:
        lista_archivos.insert(tk.END, archivo)

def obtener_seleccion(ventana_principal,ventana_archivos,lista_archivos):
    # Obtiene el índice seleccionado en la lista
    indice_seleccionado = lista_archivos.curselection()

    if indice_seleccionado:
        archivo_seleccionado = lista_archivos.get(indice_seleccionado[0])
        print(f"Archivo seleccionado: {archivo_seleccionado}")
        mostrar_tablas(ventana_principal,archivo_seleccionado)
        ventana_archivos.destroy()



def mostrar_tablas(ventana_principal,nombre_base):
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
    lista_tablas = tk.Listbox(ventana_tablas, selectmode=tk.MULTIPLE)
    lista_tablas.place(x=20,y=70,width=440,height=200)
    # Cargar automáticamente los archivos de la carpeta al iniciar
    cargar_tablas(lista_tablas,lista_nombre_tablas)

    boton_seleccionar = tk.Button(ventana_tablas, text="Cancelar", command=lambda:cancelar(ventana_tablas),bg="#A90F0F", fg="white", font=("Helvetica", 14))
    boton_seleccionar.place(x=37,y=280,width=110,height=30) 

    boton_seleccionar = tk.Button(ventana_tablas, text="Atras", command=lambda:atras(ventana_principal,ventana_tablas),bg="#A9A90F", fg="white", font=("Helvetica", 14))
    boton_seleccionar.place(x=185,y=280,width=110,height=30) 

    boton_seleccionar = tk.Button(ventana_tablas, text="Confirmar", command=lambda: obtener_seleccion_tablas(ventana_principal,ventana_tablas,lista_tablas,nombre_base),bg="#0FA926", fg="white", font=("Helvetica", 14))
    boton_seleccionar.place(x=330,y=280,width=110,height=30) 

def cargar_tablas(lista_tablas,lista_nombres):
    # Limpia la lista actual
    lista_tablas.delete(0, tk.END)

    # Agrega los nombres de los archivos a la lista
    for archivo in lista_nombres:
        lista_tablas.insert(tk.END, archivo)

def obtener_seleccion_tablas(ventana_principal,ventana_tablas,lista_tablas,nombre_base):
    indices_seleccionados = lista_tablas.curselection()
   
    if indices_seleccionados:
        archivos_seleccionados = [lista_tablas.get(indice) for indice in indices_seleccionados]
        #print(f"Archivos seleccionados: {archivos_seleccionados}")
        ruta = "BASE_DATOS/"+str(nombre_base)
        tree = ET.parse(ruta)
        root = tree.getroot()
        base_existente = None
        for base in root.findall('base'):

            #RECORRE LA LISTA DE NOMRBES
            for nombre_tabla_actual in archivos_seleccionados:
                print("TABLA: "+str(nombre_tabla_actual))
                for tabla in base.findall('tabla'):
                    
                    if(tabla.attrib['name'] == nombre_tabla_actual):
                        salida = "USE "
                        salida+=str(nombre_base[:-4])
                        salida+=";\n\n" 
                        lista_column = []
                        lista_tipos_column = []
                        lista_nulo_column = []
                        lista_foreign_column =[]
                        lista_reference_column = []
                        for campo in tabla.findall('campo'):
                            for dato in campo.findall('nombre'):    #NOMBRE
                                lista_column.append(dato.text)

                            for dato in campo.findall('tipo'):  #TIPO
                                lista_tipos_column.append(dato.text)

                            for dato in campo.findall('nulo'):  #NULO
                                lista_nulo_column.append(dato.text)

                            for dato in campo.findall('foreignkey'):  #FOREIGN
                                lista_foreign_column.append(dato.text)
                            
                            for dato in campo.findall('reference'):  #REFERENCE
                                lista_reference_column.append(dato.text)

                        #OBTENER LAS COLUMNAS
                        for campo in tabla.findall('dato'):
                            lista_valor = []
                            for dato in campo:
                                lista_valor.append(dato.text)
                            #CREAR EL INSERT
                            
                            columnas = ""
                            datos = ""
                            for i in range(len(lista_valor)):
                                columna = lista_column[i]

                                valor = lista_valor[i]
                                tipo_column = lista_tipos_column[i]
                                nulo = lista_nulo_column[i]
                                foreign = lista_foreign_column[i]
                                reference = lista_reference_column[i]

                                #VALIDAR TIPO CON COLUMNA
                                if(valor !=None):
                                    if(i !=0):
                                        datos += ", "
                                        columnas += ", "
                                    if("CHAR" in tipo_column or "VARCHAR" in tipo_column):
                                        #comando += '"'+str(valor)+'"'
                                        datos += '"'+str(valor)+'"'
                                        columnas+= str(columna)
                                    else:
                                        #comando += valor
                                        datos += str(valor)
                                        columnas += str(columna)
   
                            salida += "INSERT INTO "+str(nombre_tabla_actual)+" ("+str(columnas)+") VALUES (" +str(datos) + ");\n"
                            #print(comando)

                    with open("DATOS_EXPORTADOS/"+str(nombre_base[:-4])+"_"+str(nombre_tabla_actual)+".sql", "w") as archivo:
                        archivo.write(salida)        
                        
                            

        #EXPORTAR DATOS
        #print(salida)
        
        ventana_tablas.destroy()
        messagebox.showinfo(message="Tablas exportadas!", title="Exito")




          