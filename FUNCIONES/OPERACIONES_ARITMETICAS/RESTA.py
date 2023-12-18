from FUNCIONES.ARBOL.EJECUCION import *
from FUNCIONES.ARBOL.VALOR import *

class RESTA(Expresion):        
    def __init__(self, numero1,numero2, linea, columna):
        super().__init__(linea, columna, "RESTA")
        self.numero1 = numero1      #SON OBJETOS VALOR
        self.numero2 = numero2

    def obtener_valor(self, actual, globa, ast):
        #print(self.text)
        if(isinstance(self.numero1,Expresion) and isinstance(self.numero2,Expresion)):
            numero1 = self.numero1.obtener_valor(actual,globa,ast)
            numero2 = self.numero2.obtener_valor(actual,globa,ast)
            tipo_numero1 = self.numero1.tipo.obtener_tipo_dato()
            tipo_numero2 = self.numero2.tipo.obtener_tipo_dato()

            #VALIDACION DE TIPOS
            if(tipo_numero1 == TIPO.DATE or tipo_numero1 == TIPO.DATETIME or tipo_numero2 == TIPO.DATE or tipo_numero2 == TIPO.DATETIME): #CUALQUIER OPERACION CON DATE O DATETIME ES ERROR
                respuesta = VALOR("ERROR",TIPO.ERROR,self.linea,self.columna)
            
            elif(tipo_numero1 == TIPO.NCHAR or tipo_numero1 == TIPO.NVARCHAR or tipo_numero2 == TIPO.NCHAR or tipo_numero2 == TIPO.NVARCHAR): #CUALQUIER OPERACION CON CHAR O VARCHAR ES CONCATENAR
                respuesta = VALOR("ERROR",TIPO.ERROR,self.linea,self.columna)

            elif(tipo_numero1 == TIPO.INT or tipo_numero1 == TIPO.BIT):
                if(tipo_numero2 == TIPO.BIT or tipo_numero2 == TIPO.INT):           #INT - BIT  |   INT - INT
                    val = numero1 - numero2        
                    respuesta = VALOR(val,TIPO.INT,self.linea,self.columna)        

                elif(tipo_numero2 == TIPO.DECIMAL):                                 #INT - DECIMAL
                    val = numero1 - numero2
                    respuesta = VALOR(val,TIPO.DECIMAL,self.linea,self.columna)

            
            elif(tipo_numero1 == TIPO.DECIMAL):
                if(tipo_numero2 == TIPO.BIT or tipo_numero2 == TIPO.INT or tipo_numero2== TIPO.DECIMAL):      #DECIMAL - BIT | DECIMAL - INT | DECIMAL - DECIMAL                                 #DECIMAL - BIT
                    val = numero1 - numero2        
                    respuesta = VALOR(val,TIPO.DECIMAL,self.linea,self.columna)        

            else:
                respuesta = VALOR("ERROR",TIPO.ERROR,self.linea,self.columna)
        else:
            respuesta = VALOR("ERROR",TIPO.ERROR,self.linea,self.columna)
        #BORRAR
        ast.escribir_en_consola("LA RESPUESTA ES: "+str(respuesta.valor) +"\n")
        self.tipo = respuesta.tipo
        return respuesta.obtener_valor(actual,globa,ast)