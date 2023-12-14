from FUNCIONES.ARBOL.EJECUCION import *
from FUNCIONES.ERROR_LSS import *
from FUNCIONES.ARBOL.TABLA_FUNCIONES_VARIABLES import *
from FUNCIONES.ARBOL.NODO_TABLA_SIMBOLOS import *

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

    def guardar_en_tabla_simbolos(self,identificador,tipo_variable, tipo, entorno,linea,columna):
        nodo = NODO_TABLA_SIMBOLOS(identificador,tipo_variable,tipo,entorno,linea,columna)
        self.tabla_simbolos.append(nodo)
    
    def graficar_tabla_simbolos():
        print("NO IMPLEMENTADO")

    def graficar_reporte_errores(self): #POR AHORA SOLO MUESTRA LOS ERRORES
        for error in self.errores_codigo:
            if(isinstance(error,ERROR_LSS)):
                print(str(error.tipo) + ": "+str(error.descripcion) + " , "+str(error.linea))
