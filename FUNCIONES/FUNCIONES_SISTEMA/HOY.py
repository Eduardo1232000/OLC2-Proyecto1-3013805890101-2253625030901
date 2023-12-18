from FUNCIONES.ARBOL.EJECUCION import *
from FUNCIONES.ARBOL.VALOR import *
import datetime

class HOY(Expresion):        
    def __init__(self, linea, columna):
        super().__init__(linea, columna, "HOY")
        
    def obtener_valor(self, actual, globa, ast):
        #print(self.text)
        fecha= str(datetime.datetime.strftime(datetime.datetime.now(),"%d-%m-%Y %H:%M"))
        
        #GENERAMOS OBJETO RESPUESTA CON DATOS QUE PIDE EL ENUNCIADO
        respuesta = VALOR(fecha,TIPO.DATETIME,self.linea,self.columna)

        #BORRAR
        ast.escribir_en_consola("La fecha de hoy es: "+fecha +"\n")
        self.tipo = respuesta.tipo
        return fecha