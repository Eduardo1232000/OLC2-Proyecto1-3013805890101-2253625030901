from FUNCIONES.ARBOL.EJECUCION import *
from FUNCIONES.ARBOL.VALOR import *
from FUNCIONES.ERROR_LSS import *
from FUNCIONES.ARBOL.AST import *

import xml.etree.ElementTree as ET
import xml.dom.minidom

class EXPRESION_SELECT(Expresion):        
    def __init__(self, nombre_columna,operacion, linea, columna):
        super().__init__(linea, columna, "EXPRESION SELECT")
        self.nombre_columna = nombre_columna      #SON OBJETOS VALOR
        self.operacion = operacion
        self.numero = None

    def obtener_valor(self, actual, globa, ast):
        if(isinstance(ast,AST) and isinstance(self.nombre_tabla,VALOR) and isinstance(self.nombre_columna,VALOR)):
            nom_tabla = self.nombre_tabla.obtener_valor(actual,globa,ast)
            nom_columna = self.nombre_columna.obtener_valor(actual,globa,ast)
            base_activa = ast.obtener_base_activa()

           