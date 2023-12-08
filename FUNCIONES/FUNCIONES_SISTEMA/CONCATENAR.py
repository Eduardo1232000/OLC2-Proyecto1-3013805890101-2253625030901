from FUNCIONES.ARBOL.EJECUCION import *
from FUNCIONES.ARBOL.VALOR import *

class CONCATENAR(Expresion):        
    def __init__(self, cadena1,cadena2, linea, columna):
        super().__init__(linea, columna, "CONCATENAR")
        self.cadena1 = cadena1      #SON OBJETOS VALOR
        self.cadena2 = cadena2

    def obtener_valor(self, actual, globa, ast):
        val_respuesta = str(self.cadena1.valor) + str(self.cadena2.valor)
        respuesta = VALOR(val_respuesta,TIPO.VARCHAR,self.linea,self.columna)
        ast.escribir_en_consola("LA NUEVA CADENA ES: "+respuesta.valor +"\n")
        return respuesta
        