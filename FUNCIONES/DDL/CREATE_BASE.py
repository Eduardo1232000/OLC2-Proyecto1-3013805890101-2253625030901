from FUNCIONES.ARBOL.EJECUCION import *
from FUNCIONES.ARBOL.VALOR import *
from FUNCIONES.CREAR_BASE import *

class CREATE_BASE(Instruccion):        
    def __init__(self,nombre, linea, columna):
        super().__init__(linea, columna, "CREATE ")
   #SON OBJETOS VALOR
        self.nombre = nombre    #ES UN VALOR

    def ejecutar(self, actual, globa, ast):
        if(isinstance(self.nombre,VALOR)):
            crear_base_vacia(self.nombre.obtener_valor(actual,globa,ast))
            ast.escribir_en_consola("BASE DE DATOS CREADA!\n")