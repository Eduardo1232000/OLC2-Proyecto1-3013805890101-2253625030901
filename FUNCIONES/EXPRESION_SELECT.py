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


    def obtener_valor(self, actual, globa, ast):
        if(isinstance(ast,AST)and isinstance(self.nombre_columna,VALOR) and isinstance(self.operacion, Expresion)):
            base_activa = ast.obtener_base_activa()
            tabla_activa = ast.obtener_tabla_activa()
            nom_columna = self.nombre_columna.obtener_valor(actual,globa,ast)
            
            val = VALOR("",TIPO.EXPRESION_SELECT,self.linea, self.columna)
            self.tipo = val.tipo
            exp = self.operacion.obtener_valor(actual,globa,ast)
            print(exp)
            exp[1] = str(nom_columna)
            print(exp)
            return exp


           