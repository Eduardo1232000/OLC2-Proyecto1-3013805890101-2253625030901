from FUNCIONES.ARBOL.EJECUCION import *
from FUNCIONES.ARBOL.VALOR import *
from FUNCIONES.ERROR_LSS import *

class CAS(Expresion):        
    def __init__(self, valor1,tipo, linea, columna):
        super().__init__(linea, columna, "CAS")
        self.valor1 = valor1      #SON OBJETOS VALOR
        self.tipo = tipo


    def obtener_valor(self, actual, globa, ast):
        #print(self.text)
        if(isinstance(self.valor1,Expresion) and isinstance(self.tipo,TIPODATO)):
            valor1 = self.valor1.obtener_valor(actual,globa,ast)
            tipo_valor1 = self.valor1.tipo.obtener_tipo_dato()
            tipo_cambio =self.tipo.tipo
            if(tipo_cambio == TIPO.INT):
                if(tipo_valor1 == TIPO.BIT):
                    respuesta = VALOR(int(valor1),TIPO.INT,self.linea,self.columna)
                elif(tipo_valor1 == TIPO.NVARCHAR or tipo_valor1 == TIPO.NCHAR):
                    sumatoria = 0
                    for i in range(len(str(valor1))):
                        letra = str(valor1)[i]
                        valor_asc = ord(letra)
                        #print(valor_asc)
                        sumatoria += valor_asc
                    respuesta = VALOR(int(sumatoria),TIPO.INT,self.linea,self.columna)
                else:
                    respuesta = VALOR("ERROR",TIPO.ERROR,self.linea,self.columna)
                    ast.escribir_en_consola("("+str(self.linea)+")"+"ERROR: Valor de tipo de dato incorrecto \n")
                    ast.insertar_error_semantico(ERROR_LSS("SEMANTICO","CAS: Valor de tipo incorrecto",self.linea))  
            elif(tipo_cambio == TIPO.NVARCHAR):
                if(tipo_valor1 == TIPO.INT or tipo_valor1 == TIPO.BIT):
                    if (valor1 > 250):
                        respuesta = VALOR("",TIPO.NVARCHAR,self.linea,self.columna)
                    else:
                        if(valor1 == 0):
                            respuesta = VALOR("0",TIPO.NVARCHAR,self.linea,self.columna)
                        else:
                            respuesta = VALOR(chr(int(valor1)),TIPO.NVARCHAR,self.linea,self.columna)
                else:
                    respuesta = VALOR("ERROR",TIPO.ERROR,self.linea,self.columna) 
                    ast.escribir_en_consola("("+str(self.linea)+")"+"ERROR: Valor de tipo de dato incorrecto \n")
                    ast.insertar_error_semantico(ERROR_LSS("SEMANTICO","CAS: Valor de tipo incorrecto",self.linea))           
            else: 
                respuesta = VALOR("ERROR",TIPO.ERROR,self.linea,self.columna)
                ast.escribir_en_consola("("+str(self.linea)+")"+"ERROR: Tipo de dato incorrecto \n")
                ast.insertar_error_semantico(ERROR_LSS("SEMANTICO","CAS: Tipo incorrecto",self.linea))
            #BORRAR
            ast.escribir_en_consola("("+str(self.linea)+")"+"LA NUEVA CADENA ES: "+str(respuesta.obtener_valor(actual,globa,ast)) +"\n")
            self.tipo = respuesta.tipo
            return respuesta.obtener_valor(actual,globa,ast)