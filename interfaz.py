from tkinter import *
from tkinter import ttk
from tkinter import filedialog      #ABRIR ARCHIVOS
from tkinter import messagebox      #MOSTRAR UN MENSAJE AL USUARIO
import os       #PARA OBTENER EL NOMBRE DEL ARCHIVO

from FUNCIONES.LECTURA_XML import *
from FUNCIONES.RESALTADO import *
from FUNCIONES.CREAR_BASE import *

from FUNCIONES.ARBOL.AST import *

from FUNCIONES.EXPORTAR_IMPORTAR.EXPORTAR import *
from FUNCIONES.EXPORTAR_IMPORTAR.IMPORTAR import *
from FUNCIONES.CREAR_REPORTES.MOSTRAR_REPORTES import *
import gramatica

contador_querys  = 1
ruta_query_actual = ""
class interfaz:
    def __init__(self, ventana):
        self.ventana = ventana  #INICIALIZAMOS LA VENTANA
        self.ventana.title("PROYECTO - COMPILADORES 2") #TITULO DE VENTANA
        self.ventana.geometry("1280x720")    #TAMAÑO DE LA VENTANA
        self.ventana.configure(bg="#1A1C2F")#color de fondo ventana

        self.ventana.resizable(width=False, height=False)

        
def crear_pestana(notebook,texto_prueba):
    pestana = Frame(notebook)
    notebook.add(pestana, text = texto_prueba)
    contenido = Text(pestana,font=("Helvetica", 12))
    contenido.configure(bg="#ECEEF1")
    contenido.place(x=0,y=0,width=1000,height=300)

    contenido = Label(pestana,text=str(texto_prueba),state="disabled")       #PARA GUARDAR LA RUTA DEL ARCHIVO SI SE ABRIO UNO
    contenido = Label(pestana,text="",state="disabled")       #RUTA ERRORES
    contenido = Label(pestana,text="",state="disabled")       #RUTA TABLA
    contenido = Label(pestana,text="",state="disabled")       #RUTA ARBOL



def cargar_datos_arbol():
    #BUSCAR LAS BASES DE DATOS Y FORMAR ESTA ESTRUCTURA
    try:
        #AGREGAR FUNCIONES
        arbol.delete(*arbol.get_children())
        baa = construir_estructura_arbol_xml()
        for dato in baa:
            ba = dato
            bas = arbol.insert("",'end',text=ba[0])
            for i in range(1,4):
                pa = ""
                if(i == 1):
                    pa = arbol.insert(bas,'end',text="Tablas")
                elif(i == 2):
                    pa = arbol.insert(bas,'end',text = "Funciones")
                elif(i==3):
                    pa = arbol.insert(bas,'end',text = "Procedimientos")
                for j in ba[i]:
                    arbol.insert(pa,'end',text = j)    
    except:
        print("NO HAY ARBOLES")

def accion_menu_archivo(opcion):    #ACCION DEL MENU ARCHIVO
    global contador_querys
    pestana_actual = cuaderno.select()
    contenido_texto, label1,r_errores,r_tabla,r_arbol = cuaderno.nametowidget(pestana_actual).winfo_children()
    if(opcion == "nuevo"):
        crear_pestana(cuaderno, "Query"+str(int(contador_querys) +1))
        if(int(contador_querys>0)):
            contador_querys +=1
    elif(opcion == "abrir"):
        pestana_actual = cuaderno.select()  #OBTENCION DE CODIGO DE LA pestana ACTUAL

        archivo_seleccionado = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Archivos de texto", "*.sql"), ("Todos los archivos", "*.*")])
        if archivo_seleccionado:
            with open(archivo_seleccionado, "r") as archivo:
                contenido = archivo.read()
                contenido_texto.delete(1.0, END) 
                contenido_texto.insert(END, contenido)

                #MODIFICAR LA RUTA DEL ARCHIVO EN MEMORIA
                label1.config(text=archivo_seleccionado)   #GUARDAMOS LA RUTA EN LA pestana

                nombre = os.path.basename(archivo_seleccionado)     #OBTENEMOS EL NOMBRE DEL ARCHIVO
                indice_pestana = cuaderno.index(pestana_actual)     #CAMBIAMOS EL NOMBRE DE LA PESTANA
                cuaderno.tab(indice_pestana, text=nombre)

    elif(opcion == "guardar"):
        pestana_actual = cuaderno.select()  #OBTENCION DE CODIGO DE LA pestana ACTUAL
       #OBTENER EL CONTENIDO DEL AREA DE TEXTO
        contenido = contenido_texto.get("1.0", END)

        #OBTENER EL CONTENIDO DEL LABEL OCULTO
        ruta = label1.cget("text")

        if(ruta !=""):                   #SI EXISTE ALGUNA RUTA GUARDADA GUARDARLO AHI
            with open(ruta, "w") as archivo:
                archivo.write(contenido)
                messagebox.showinfo(message="Archivo Guardado con exito!", title="Aviso")
        else:                                       #SI NO ES UN GUARDAR COMO
            archivo_seleccionado = filedialog.asksaveasfilename(defaultextension=".sql", filetypes=[("Archivos de texto", "*.sql"), ("Todos los archivos", "*.*")])
            if archivo_seleccionado:
                with open(archivo_seleccionado, "w") as archivo:
                    archivo.write(contenido)
                messagebox.showinfo(message="Archivo Guardado con exito!", title="Aviso")

                contenido_texto.config(text=archivo_seleccionado)   #GUARDAMOS LA RUTA EN LA pestana
                nombre = os.path.basename(archivo_seleccionado)     #OBTENEMOS EL NOMBRE DEL ARCHIVO
                indice_pestana = cuaderno.index(pestana_actual)     #CAMBIAMOS EL NOMBRE DE LA PESTANA
                cuaderno.tab(indice_pestana, text=nombre)

    elif(opcion == "guardarcomo"):
        contenido = contenido_texto.get("1.0", END)        
        
        archivo_seleccionado = filedialog.asksaveasfilename(defaultextension=".sql", filetypes=[("Archivos de texto", "*.sql"), ("Todos los archivos", "*.*")])
        if archivo_seleccionado:
            with open(archivo_seleccionado, "w") as archivo:
                archivo.write(contenido)
            messagebox.showinfo(message="Archivo Guardado con exito!", title="Aviso")

        label1
        label1.config(text=archivo_seleccionado)   #GUARDAMOS LA RUTA EN LA pestana
        nombre = os.path.basename(archivo_seleccionado)     #OBTENEMOS EL NOMBRE DEL ARCHIVO
        indice_pestana = cuaderno.index(pestana_actual)     #CAMBIAMOS EL NOMBRE DE LA PESTANA
        cuaderno.tab(indice_pestana, text=nombre)

    elif(opcion == "cerrar"):
        indice_pestana = cuaderno.index(pestana_actual)
        cuaderno.forget(indice_pestana)
    else:
        ventana_principal.destroy()

def accion_menu_herramientas(opcion):   #ACCION DEL MENU HERRAMIENTAS
    global contador_querys
    pestana_actual = cuaderno.select()
    contenido_texto, label1,r_errores,r_tabla,r_arbol = cuaderno.nametowidget(pestana_actual).winfo_children()
    if(opcion == "crear_base"):
        nombre = simpledialog.askstring("Ingresar Nombre", "Por favor, ingresa el nombre de tu base de datos:")
        if nombre:
            respuesta = crear_base_vacia(str(nombre))
            if(respuesta == True):
                cargar_datos_arbol()
                messagebox.showinfo("Exito", "Base de Datos: "+str(nombre) + " Creada!")
            else:
                messagebox.showerror("Error", "Ya existe una Base de Datos con ese nombre !")
    elif(opcion == "eliminar_base"):
        nombre = simpledialog.askstring("Ingresar Nombre", "Por favor, ingresa el nombre de tu base de datos:")
        if nombre:
            try:
                ruta = "BASE_DATOS/" + str(nombre) + ".xml"
                os.remove(ruta)
                cargar_datos_arbol()
                messagebox.showinfo("Exito", "Base de Datos: "+str(nombre) + " Eliminada!")
            except FileNotFoundError:
                messagebox.showerror("Error", "Base de Datos: "+str(nombre) + " No existe!")
            except Exception as e:
                print(f"Error al intentar eliminar el archivo '{nombre}': {e}")
                messagebox.showerror("Error", "Error al intentar eliminar la base "+str(nombre)+".")

    elif(opcion == "crear_dump"):
        print("Base Datos - DUMP")
    elif(opcion == "seleccionar_base"):
        print("Base Datos - Seleccionar")

    elif(opcion == "nuevo_query"):
        crear_pestana(cuaderno, "Query"+str(int(contador_querys) +1))
        if(int(contador_querys>0)):
            contador_querys +=1
    elif(opcion == "ejecutar_query"):
        contenido = contenido_texto.get("1.0", END)
        
        #ANALIZAR CONTENIDO
        respuesta_parser = gramatica.parses(contenido)
        if(respuesta_parser is not None):
            respuesta = respuesta_parser[0]
        
            if(respuesta == None or respuesta == "" or respuesta == []):
                print("",end="")
            else:
                arbol_sintactico = AST(respuesta,respuesta_parser[1],respuesta_parser[2])
                arbol_sintactico.ejecutar()
                arbol_sintactico.graficar_reporte_errores(cuaderno)
                arbol_sintactico.graficar_tabla_simbolos(cuaderno)
                #COMO YA SE EJECUTO PODEMOS MOSTRAR LA SALIDA

                salida.config(state='normal')  #ASIGNAR CONTENIDO A SALIDA (PARA PRUEBAS)
                salida.delete(1.0, END) 
                salida.insert(END, arbol_sintactico.obtener_salida())  
                salida.config(state='disabled')
                cargar_datos_arbol()        #ACTUALIZAR VISTA ARBOL
    

    elif(opcion == "exportar"):
        mostrar_bases(ventana_principal)

    elif(opcion == "importar"):
        importar_datos()

    else:
        ventana_principal.destroy()

def mostrar_menu_archivo(): #ACCION BOTON ARCHIVO
    menu_archivo.post(boton_archivo.winfo_rootx(),boton_archivo.winfo_rooty()+boton_archivo.winfo_height())

def mostrar_menu_herramientas(): #ACCION BOTON HERRAMIENTAS
    menu_herramientas.post(boton_herramientas.winfo_rootx(),boton_herramientas.winfo_rooty()+boton_herramientas.winfo_height())

def actualizar_resaltar_palabras(event=None):
    resaltar_palabras(contenido_texto)

def mostrar_reporte_errores(ventana_principal,cuaderno,tipo):
    print(tipo)
    pestana_actual = cuaderno.select()
    contenido_texto, label1,r_errores,r_tabla,r_arbol = cuaderno.nametowidget(pestana_actual).winfo_children()
    ruta_errores = r_errores.cget("text")
    ruta_tabla = r_tabla.cget("text")
    ruta_arbol = r_arbol.cget("text")
    if(tipo == "ERRORES" and (ruta_errores !="")):
        mostrar_reporte(ventana_principal,ruta_errores, "REPORTE DE ERRORES")
    elif(tipo == "TABLA" and (ruta_tabla !="")):
        mostrar_reporte(ventana_principal,ruta_tabla, "REPORTE DE TABLA DE SIMBOLOS")
    elif(tipo == "ARBOL" and (ruta_arbol !="")):
        mostrar_reporte(ventana_principal,ruta_arbol,"REPORTE DE AST")
    else:
        messagebox.showerror(message="aun no se ha generado este reporte!", title="Error")

ventana_principal = Tk()    #CREAMOS LA VENTANA PRINCIPAL                             
programa = interfaz(ventana_principal)

titulo = Label(ventana_principal, text="XSQL-IDE", font=("Helvetica", 16))          #TITULO
titulo.configure(bg="#252950",fg="white")
titulo.place(x=0,y=0,width=1280,height=60)

#BOTONES DE REPORTES
boton_reporte_errores = Button(ventana_principal, text="Errores",bg="#9C8442", fg="white",font=("Helvetica", 12),command=lambda:mostrar_reporte_errores(ventana_principal,cuaderno,"ERRORES"))
boton_reporte_errores.place(x=900,y=20, width=100, height=30)

#BOTONES DE REPORTES
boton_reporte_tabla = Button(ventana_principal, text="Tabla de Simbolos",bg="#9C8442", fg="white",font=("Helvetica", 12),command=lambda:mostrar_reporte_errores(ventana_principal,cuaderno,"TABLA"))
boton_reporte_tabla.place(x=1000,y=20, width=150, height=30)

#BOTONES DE REPORTES
boton_reporte_ast = Button(ventana_principal, text="Arbol",bg="#9C8442", fg="white",font=("Helvetica", 12),command=lambda:mostrar_reporte_errores(ventana_principal,cuaderno,"ARBOL"))
boton_reporte_ast.place(x=1150,y=20, width=100, height=30)

boton_archivo = Button(ventana_principal, text="Archivo",bg="#4F5C7C", fg="white",font=("Helvetica", 12),command=mostrar_menu_archivo)
boton_archivo.place(x=10,y=65, width=100, height=30)
menu_archivo = Menu(boton_archivo, tearoff=0)
menu_archivo.add_command(label="Nuevo",command=lambda:accion_menu_archivo("nuevo"))
menu_archivo.add_command(label="Abrir",command=lambda:accion_menu_archivo("abrir"))
menu_archivo.add_command(label="Guardar",command=lambda:accion_menu_archivo("guardar"))
menu_archivo.add_command(label="Guardar Como",command=lambda:accion_menu_archivo("guardarcomo"))
menu_archivo.add_command(label="Cerrar",command=lambda:accion_menu_archivo("cerrar"))
menu_archivo.add_command(label="Salir",command=lambda:accion_menu_archivo("salir"))

boton_archivo.bind("<Button-1>",lambda event: None) 

boton_herramientas = Button(ventana_principal, text="Herramientas",bg="#4F5C7C", fg="white",font=("Helvetica", 12),command=mostrar_menu_herramientas)
boton_herramientas.place(x=110,y=65, width=100, height=30)

menu_herramientas = Menu(boton_archivo, tearoff=0)
submenu_base_datos = Menu(boton_archivo, tearoff=0)
submenu_base_datos.add_command(label="Crear Base de Datos",command=lambda:accion_menu_herramientas("crear_base"))
submenu_base_datos.add_command(label="Eliminar Base de Datos",command=lambda:accion_menu_herramientas("eliminar_base"))
submenu_base_datos.add_command(label="Crear DUMP",command=lambda:accion_menu_herramientas("crear_dump"))
submenu_base_datos.add_command(label="Seleccionar Base de Datos",command=lambda:accion_menu_herramientas("seleccionar_base"))

submenu_sql = Menu(boton_archivo, tearoff=0)
submenu_sql.add_command(label="Nuevo Query",command=lambda:accion_menu_herramientas("nuevo_query"))
submenu_sql.add_command(label="Ejecutar Query",command=lambda:accion_menu_herramientas("ejecutar_query"))

menu_herramientas.add_cascade(label="Base de Datos",menu=submenu_base_datos)        #AGREGAR LOS SUBMENUS AL MENU HERRAMIENTAS
menu_herramientas.add_cascade(label="SQL",menu=submenu_sql)
menu_herramientas.add_command(label="Exportar",command=lambda:accion_menu_herramientas("exportar"))
menu_herramientas.add_command(label="Importar",command=lambda:accion_menu_herramientas("importar"))

boton_herramientas.bind("<Button-1>",lambda event: None)

vista_arbol = Frame(ventana_principal)  #CREAMOS EL CONTENEDOR DE LA VISTA DE ARBOL
vista_arbol.configure(bg='red')
vista_arbol.place(x=10,y=100,width=230,height=600)


arbol = ttk.Treeview(vista_arbol)
arbol.pack(side="left", fill="both", expand=True)



scrollbar = ttk.Scrollbar(vista_arbol, orient="vertical", command=arbol.yview)  #SCROLLBAR PARA EL ARBOL
scrollbar.pack(side="right", fill="y")
arbol.configure(yscrollcommand=scrollbar.set )
arbol
cargar_datos_arbol()

area_query = Frame(ventana_principal)       #CREAMOS EL CONTENEDOR DE pestanaS
area_query.configure(bg='blue')
area_query.place(x=250,y=100,width=1000,height=320)
cuaderno = ttk.Notebook(area_query)
crear_pestana(cuaderno, "Query1")
cuaderno.pack(expand=True, fill='both')

label_salida = Label(ventana_principal, text="Salida de Datos",font=("Helvetica", 12)) #CREAMOS EL TEXT PARA SALIDA
label_salida.place(x=250,y=425,height=25)

salida= Text(ventana_principal,state='disabled',font=("Helvetica", 12))
salida.configure(bg="#ECEEF1")
salida.place(x=250, y=450, width=1000, height=250)

#VINCULAR FUNCION RESALTAR PALABRAS CLAVE
pestana_actual = cuaderno.select()  #OBTENCION DE CODIGO DE LA pestana ACTUAL
contenido_texto = cuaderno.nametowidget(pestana_actual).children['!text']

contenido_texto.bind('<KeyRelease>', actualizar_resaltar_palabras)
#INICIALIZAMOS VENTANA
ventana_principal.mainloop()