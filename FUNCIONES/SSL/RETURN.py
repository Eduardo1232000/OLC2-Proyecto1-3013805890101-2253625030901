from FUNCIONES.ARBOL.EJECUCION import *
from FUNCIONES.ARBOL.VALOR import *

class RETURN(Instruccion):        
    def __init__(self, expresion, linea, columna):
        super().__init__(linea, columna, "RETURN")
        self.expresion = expresion      #SON OBJETOS VALOR


    def ejecutar(self, actual, globa, ast):
        if(isinstance(self.expresion,Expresion)):
            self.ejecuto_return = self.expresion
            