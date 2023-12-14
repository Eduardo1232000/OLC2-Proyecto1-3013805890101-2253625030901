from FUNCIONES.ARBOL.DATOS_EJECUCION import *
from abc import abstractmethod
class Instruccion(ListaEjecuciones):                    # INSTRUCCION NO RETORNA NADA  (asignaciones, crear tablas etc...)
    def __init__(self, linea, columna, nombre_in_ex):
        super().__init__(linea, columna, nombre_in_ex)

    @abstractmethod
    def ejecutar(self, actual, globa, ast):
        pass

class Expresion(ListaEjecuciones):                      #EXPRESION RETORNA VALOR (suma, resta, comparaciones etc...)
    def __init__(self, linea, columna, nombre_in_ex):
        super().__init__(linea, columna, nombre_in_ex)
        self.tipo = ""

    @abstractmethod
    def obtener_valor(self, actual, globa, ast):
        pass