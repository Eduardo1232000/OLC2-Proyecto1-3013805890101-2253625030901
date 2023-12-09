from FUNCIONES.ARBOL.EJECUCION import *
from FUNCIONES.ARBOL.VALOR import *

class EXP_NOT(Expresion):        
    def __init__(self, expr1, linea, columna):
        super().__init__(linea, columna, "NOT")
        self.expr1 = expr1      #SON OBJETOS VALOR

    def obtener_valor(self, actual, globa, ast):
        if(isinstance(self.expr1,VALOR)):
            expr1 = self.expr1.obtener_valor(actual,globa,ast)
            tipo_expr1 = self.expr1.tipo.obtener_tipo_dato()

            if(((tipo_expr1==TIPO.INT or tipo_expr1==TIPO.BIT or tipo_expr1==TIPO.DECIMAL))):
                if((int(expr1)==0 or int(expr1)==1)):
                    if(expr1 == 1):
                        respuesta = VALOR(0,TIPO.BIT,self.linea,self.columna)   #1= VERDADERO
                    else:
                        respuesta = VALOR(1,TIPO.BIT,self.linea,self.columna)   #1= VERDADERO
                else:
                    respuesta = VALOR("ERROR",TIPO.ERROR,self.linea,self.columna)   #0= FALSO

            #EXTRA PORQUE NO SE ENTRA TAMBIEN
            elif((tipo_expr1 == TIPO.CHAR or tipo_expr1 == TIPO.VARCHAR)):
                if(expr1.lower() == "verdadero"):
                    respuesta = VALOR(0,TIPO.BIT,self.linea,self.columna)
                elif (expr1.lower() == "falso"):
                    respuesta = VALOR(1,TIPO.BIT,self.linea,self.columna)
                
                else:
                    respuesta = VALOR("ERROR",TIPO.ERROR,self.linea,self.columna)
            else:
                respuesta = VALOR("ERROR",TIPO.ERROR,self.linea,self.columna) 
            
        else:
            respuesta = VALOR("ERROR",TIPO.ERROR,self.linea,self.columna)
        #BORRAR
        ast.escribir_en_consola("LA RESPUESTA ES: "+str(respuesta.valor) +"\n")
        return respuesta