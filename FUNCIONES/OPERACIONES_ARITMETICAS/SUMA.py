from FUNCIONES.ARBOL.EJECUCION import *
from FUNCIONES.ARBOL.VALOR import *

class SUMA(Expresion):        
    def __init__(self, numero1,numero2, linea, columna):
        super().__init__(linea, columna, "SUMA")
        self.numero1 = numero1      #SON OBJETOS VALOR
        self.numero2 = numero2

    def obtener_valor(self, actual, globa, ast):
        if(isinstance(self.numero1,VALOR) and isinstance(self.numero2,VALOR)):
            numero1 = self.numero1.obtener_valor(actual,globa,ast)
            numero2 = self.numero2.obtener_valor(actual,globa,ast)
            tipo_numero1 = self.numero1.tipo.obtener_tipo_dato()
            tipo_numero2 = self.numero2.tipo.obtener_tipo_dato()

            #VALIDACION DE TIPOS
            if(tipo_numero1 == TIPO.DATE or tipo_numero1 == TIPO.DATETIME or tipo_numero2 == TIPO.DATE or tipo_numero2 == TIPO.DATETIME): #CUALQUIER OPERACION CON DATE O DATETIME ES ERROR
                respuesta = VALOR("ERROR",TIPO.ERROR,self.linea,self.columna)
            
            elif(tipo_numero1 == TIPO.CHAR or tipo_numero1 == TIPO.VARCHAR or tipo_numero2 == TIPO.CHAR or tipo_numero2 == TIPO.VARCHAR): #CUALQUIER OPERACION CON CHAR O VARCHAR ES CONCATENAR
                val = str(numero1) + str(numero2)
                respuesta = VALOR(val,TIPO.VARCHAR,self.linea,self.columna)

            elif(tipo_numero1 == TIPO.BIT):
                if(tipo_numero2 == TIPO.BIT):                                       #BIT - BIT
                    val = numero1 or numero2        
                    respuesta = VALOR(val,TIPO.BIT,self.linea,self.columna)        

                elif(tipo_numero2 == TIPO.INT):                                     #BIT - INT
                    val = numero1 + numero2
                    respuesta = VALOR(val,TIPO.INT,self.linea,self.columna)

                elif(tipo_numero2 == TIPO.DECIMAL):                                 #BIT - DECIMAL
                    val = numero1 + numero2
                    respuesta = VALOR(val,TIPO.DECIMAL,self.linea,self.columna)


            elif(tipo_numero1 == TIPO.INT):
                if(tipo_numero2 == TIPO.BIT or tipo_numero2 == TIPO.INT):           #INT - BIT  |   INT - INT
                    val = numero1 + numero2        
                    respuesta = VALOR(val,TIPO.INT,self.linea,self.columna)        

                elif(tipo_numero2 == TIPO.DECIMAL):                                 #INT - DECIMAL
                    val = numero1 + numero2
                    respuesta = VALOR(val,TIPO.DECIMAL,self.linea,self.columna)

            
            elif(tipo_numero1 == TIPO.DECIMAL):
                if(tipo_numero2 == TIPO.BIT or tipo_numero2 == TIPO.INT or tipo_numero2== TIPO.DECIMAL):      #DECIMAL - BIT | DECIMAL - INT | DECIMAL - DECIMAL                                 #DECIMAL - BIT
                    val = numero1 + numero2        
                    respuesta = VALOR(val,TIPO.DECIMAL,self.linea,self.columna)        

            else:
                respuesta = VALOR(0,TIPO.ERROR,self.linea,self.columna)
        else:
            respuesta = VALOR(0,TIPO.ERROR,self.linea,self.columna)
        #BORRAR
        ast.escribir_en_consola("LA RESPUESTA ES: "+str(respuesta.valor) +"\n")
        return respuesta