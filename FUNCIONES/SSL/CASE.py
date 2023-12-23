from FUNCIONES.ARBOL.EJECUCION import *
from FUNCIONES.ARBOL.VALOR import *
from FUNCIONES.ERROR_LSS import *
from FUNCIONES.ARBOL.TABLA_FUNCIONES_VARIABLES import *
from FUNCIONES.SSL.RETURN import *

class EXP_CASE(Expresion):        
    def __init__(self,lista_whens,exp_else,linea, columna):
        super().__init__(linea, columna, "CASE")
        self.lista_whens = lista_whens
        self.exp_else = exp_else

    def obtener_valor(self, actual, globa, ast):
        print(self.text)
        condicion_else = self.exp_else.obtener_valor(actual,globa,ast)
        tipo_else = self.exp_else.tipo
        for when in self.lista_whens:
            condicion = when[0].obtener_valor(actual,globa,ast)
            condicion_true = when[1].obtener_valor(actual,globa,ast)  
            if(str(condicion) == str(1)):
                self.tipo = when[1].tipo
                return condicion_true
        self.tipo = tipo_else
        return condicion_else