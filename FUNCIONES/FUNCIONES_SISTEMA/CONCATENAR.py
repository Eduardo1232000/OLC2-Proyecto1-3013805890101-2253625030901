from FUNCIONES.ARBOL.EJECUCION import *
from FUNCIONES.ARBOL.VALOR import *
from FUNCIONES.ERROR_LSS import *

class CONCATENAR(Expresion):        
    def __init__(self, cadena1,cadena2, linea, columna):
        super().__init__(linea, columna, "CONCATENAR")
        self.cadena1 = cadena1      #SON OBJETOS VALOR
        self.cadena2 = cadena2

    def obtener_valor(self, actual, globa, ast):
        #print(self.text)
        if(isinstance(self.cadena1,Expresion) and isinstance(self.cadena2,Expresion)):
            cadena1 = self.cadena1.obtener_valor(actual,globa,ast)
            cadena2 = self.cadena2.obtener_valor(actual,globa,ast)
            
            #VALIDACION DE TIPOS
            if(((self.cadena1.tipo.obtener_tipo_dato() == TIPO.NVARCHAR or self.cadena1.tipo.obtener_tipo_dato() == (TIPO.NCHAR)) and (self.cadena2.tipo.obtener_tipo_dato() == TIPO.NVARCHAR or self.cadena2.tipo.obtener_tipo_dato() == TIPO.NCHAR))):
                val_respuesta = cadena1 + cadena2
            else:
                ast.escribir_en_consola("ERROR: No se pudo reconocer el tipo de dato de los valores")
                ast.insertar_error_semantico(ERROR_LSS("SEMANTICO","CONCATENAR: No se pudo reconocer el tipo de dato de los valores",self.linea))
                respuesta = VALOR("ERROR",TIPO.ERROR,self.linea,self.columna)
                self.tipo = respuesta.tipo
                return "ERROR"

        #GENERAMOS OBJETO RESPUESTA CON DATOS QUE PIDE EL ENUNCIADO
        respuesta = VALOR(val_respuesta,TIPO.NVARCHAR,self.linea,self.columna)

        #BORRAR
        ast.escribir_en_consola("LA NUEVA CADENA ES: "+respuesta.valor +"\n")
        self.tipo = respuesta.tipo
        return val_respuesta