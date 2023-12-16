from FUNCIONES.ARBOL.EJECUCION import *
from FUNCIONES.ERROR_LSS import *
from FUNCIONES.ARBOL.TABLA_FUNCIONES_VARIABLES import *
from FUNCIONES.ARBOL.NODO_TABLA_SIMBOLOS import *
from FUNCIONES.CREAR_REPORTES.REPORTE_ERRORES import *

from REPORTES.CREAR_GRAFO import *
import os
import sys

class AST:
    def __init__(self, ejecuciones,errores_lexicos,errores_sintacticos):
        self.EJECUCIONES = ejecuciones   #LISTADO DE OBJETOS PARA EJECUTAR
        self.salida_cadena = ""  #SALIDA DE TEXTO QUE SE MUESTRA EN CONSOLA
        self.codigo_grafica=""   #CODIGO DE GRAPHVIZ DEL ARBOL
        self.tabla_simbolos=[]   #TABLA DE SIMBOLOS DEL CODIGO
        self.errores_codigo =[]
        for error in errores_lexicos:
            self.errores_codigo.append(error)
        for error in errores_sintacticos:
            self.errores_codigo.append(error)

        self.base_actual = ""
        self.tabla_actual = ""

    
    def ejecutar(self):
        #CREAMOS EL AMBITO ACTUAL Y GLOBAL
        TABLA_FUNCIONES_Y_VARIABLES_GLOBAL = TABLA_FUNCIONES_Y_VARIABLES(None,"global")     #AMBITO GLOBAL
        TABLA_FUNCIONES_Y_VARIABLES_ACTUAL = TABLA_FUNCIONES_Y_VARIABLES_GLOBAL             #AMBITO ACTUAL ES EL GLOBAL PORQUE ES EL INICIO
        for instr in self.EJECUCIONES:
            
            if isinstance(instr,Instruccion):
                instr.ejecutar(TABLA_FUNCIONES_Y_VARIABLES_ACTUAL,TABLA_FUNCIONES_Y_VARIABLES_GLOBAL,self)


            elif(isinstance(instr, Expresion)):                 #SI EN EL ARBOL APARECE UNA EXPRESION SOLO ASI, DA IGUAL EL VALOR PORQUE ASI SE HIZO EN EL IDE
                instr.obtener_valor(TABLA_FUNCIONES_Y_VARIABLES_ACTUAL,TABLA_FUNCIONES_Y_VARIABLES_GLOBAL,self)     # ES DECIR QUE SOLO ESCRIBIERON 1+1 Y NO LO ASIGNARON A ALGUNA VARIABLE

        #YA DEBE TENER LAS RESPUESTAS DE CADA OPERACION 
        print(self.salida_cadena)   #BORRAR SI NO SE QUIERE VER LAS RESPUESTAS DE CONSOLA

    def escribir_en_consola(self,texto):    #ESCRIBIR EN LA CONSOLA
        self.salida_cadena += str(texto)

    def obtener_salida(self):
        return(self.salida_cadena)
    
    def usar_base(self, nombre):
        self.base_actual = nombre

    def obtener_base_activa(self):
        return(str(self.base_actual))
    
    def usar_tabla(self,nombre):
        self.tabla_actual = nombre

    def obtener_tabla_activa(self):
        return(str(self.tabla_actual))
    def graficar(nodos):
        print("NO IMPLEMENTADO")

    def guardar_en_tabla_simbolos(self,identificador,tipo_variable,base, tipo, entorno,linea,columna):

        #VALIDAR SI EXISTE
        for nodo_t in self.tabla_simbolos:
            if(isinstance(nodo_t,NODO_TABLA_SIMBOLOS)):
                if(identificador == nodo_t.obtener_identificador()):
                    if(tipo_variable == nodo_t.obtener_tipo_var_fun()):
                        if(base == nodo_t.obtener_base()):
                            if(tipo == nodo_t.obtener_tipo()):
                                if(entorno == nodo_t.obtener_entorno):
                                    #TODO ES IGUAL, NO SE INSERTA
                                    return
        nodo = NODO_TABLA_SIMBOLOS(identificador,base,tipo_variable,tipo,entorno,linea,columna)
        self.tabla_simbolos.append(nodo)
    
    def graficar_tabla_simbolos():
        print("NO IMPLEMENTADO")

    def insertar_error_semantico(self,error):
        self.errores_codigo.append(error)

    def graficar_reporte_errores(self, ventana_principal,cuaderno): # VENTANA PRINCIPAL PARA CREAR UNA SUBVENTANA, CUADERNO PARA ALMACENAR EL NOMBRE DE LA IMAGEN
        codigo_graf_error = obtener_codigo_grafica_reporte_errores(self.errores_codigo)
        #print(codigo_graf_error)
        pestana_actual = cuaderno.select()
        contenido_texto, label1,r_errores,r_tabla,r_arbol = cuaderno.nametowidget(pestana_actual).winfo_children()
        ruta = "REPORTES/"
        nombre_archivo_se, extension = os.path.splitext(os.path.basename(str(label1.cget("text"))))
        nombre_archivo_se = nombre_archivo_se.replace(" ","_")
        ruta+=str(nombre_archivo_se)
        r_errores.config(text=ruta+".png")
        crear_grafo(codigo_graf_error,ruta)
        print("GRAFO CREADO")
