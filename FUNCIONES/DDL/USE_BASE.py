from FUNCIONES.ARBOL.EJECUCION import *
from FUNCIONES.ARBOL.VALOR import *
from FUNCIONES.CREAR_BASE import *
from FUNCIONES.ARBOL.AST import *

class USE_BASE(Instruccion):        
    def __init__(self,nombre, linea, columna):
        super().__init__(linea, columna, "USE BASE ")
   #SON OBJETOS VALOR
        self.nombre = nombre    #ES UN VALOR

    def ejecutar(self, actual, globa, ast):
        if(isinstance(self.nombre,Expresion)):
            nombre = self.nombre.obtener_valor(actual,globa,ast)
            ruta = "BASE_DATOS/"+str(nombre)+".xml"
            if os.path.exists(ruta):   #SI YA EXISTE LA BASE DE DATOS
                if(isinstance(ast, AST)):
                    ast.usar_base(nombre)
                    ast.escribir_en_consola("SE VA A UTILIZAR LA BASE: "+str(nombre)+"\n")
                    #GUARDAR CADA PROCEDIMIENTO FUNCION ETC EN SUS RESPECTIVAS LISTAS

            else:   #SI NO EXISTE LA BASE DE DATOS
                ast.escribir_en_consola("NO EXISTE LA BASE DE DATOS: "+str(nombre)+"\n")