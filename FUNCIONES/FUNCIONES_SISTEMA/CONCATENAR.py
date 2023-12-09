from FUNCIONES.ARBOL.EJECUCION import *
from FUNCIONES.ARBOL.VALOR import *

class CONCATENAR(Expresion):        
    def __init__(self, cadena1,cadena2, linea, columna):
        super().__init__(linea, columna, "CONCATENAR")
        self.cadena1 = cadena1      #SON OBJETOS VALOR
        self.cadena2 = cadena2

    def obtener_valor(self, actual, globa, ast):
        if(isinstance(self.cadena1,VALOR) and isinstance(self.cadena2,VALOR)):
            cadena1 = self.cadena1.obtener_valor(actual,globa,ast)
            cadena2 = self.cadena2.obtener_valor(actual,globa,ast)
            
            #VALIDACION DE TIPOS
            if(self.cadena1.tipo.obtener_tipo_dato() == TIPO.VARCHAR and self.cadena2.tipo.obtener_tipo_dato() == TIPO.VARCHAR):
                val_respuesta = cadena1 + cadena2

        #GENERAMOS OBJETO RESPUESTA CON DATOS QUE PIDE EL ENUNCIADO
        respuesta = VALOR(val_respuesta,TIPO.VARCHAR,self.linea,self.columna)

        #BORRAR
        ast.escribir_en_consola("LA NUEVA CADENA ES: "+respuesta.valor +"\n")
        return respuesta