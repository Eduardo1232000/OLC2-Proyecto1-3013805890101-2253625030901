from FUNCIONES.ARBOL.EJECUCION import *
from FUNCIONES.ARBOL.VALOR import *
from FUNCIONES.CREAR_BASE import *
from FUNCIONES.ERROR_LSS import *

class CREATE_BASE(Instruccion):        
    def __init__(self,nombre, linea, columna):
        super().__init__(linea, columna, "CREATE ")
   #SON OBJETOS VALOR
        self.nombre = nombre    #ES UN VALOR

    def ejecutar(self, actual, globa, ast):
        if(isinstance(self.nombre,Expresion)):
            respuesta = crear_base_vacia(self.nombre.obtener_valor(actual,globa,ast))
            if(respuesta == False):
                ast.escribir_en_consola("ERROR: Ya existe una base de datos con ese nombre!\n")
                ast.insertar_error_semantico(ERROR_LSS("SEMANTICO","CREATE: Ya existe una base de datos con ese nombre",self.linea))
            else:
                ast.escribir_en_consola("BASE DE DATOS CREADA!\n")

    '''def retornar_codigo_origen(self):
        codigo_origen = "CREATE DATA BASE "+str(self.nombre.retornar_codigo_origen()) +";"
        return codigo_origen'''