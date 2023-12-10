from FUNCIONES.ARBOL.EJECUCION import *
from FUNCIONES.ARBOL.VALOR import *
from FUNCIONES.BORRAR_BASE import *

class DROP_BASE(Instruccion):
    def __init__(self, drop_type, nombre, linea, columna):
        super().__init__(linea, columna, "DROP")
        self.drop_type = drop_type #DATABASE o TABLe
        self.nombre = nombre

    def ejecutar(self, actual, globa, ast):
        nombre_base = self.nombre.obtener_valor(actual, globa, ast)
        borrar_base(nombre_base, ast)

def procesar_drop(t, ast):
    drop_type= t[2]
    nombre_base = t[3]
    return DROP_BASE(drop_type, nombre_base, t.lineno, t.lexpos)