from FUNCIONES.ARBOL.EJECUCION import *
from FUNCIONES.ARBOL.VALOR import *

class EXP_OR(Expresion):        
    def __init__(self, expr1,expr2, linea, columna):
        super().__init__(linea, columna, "OR")
        self.expr1 = expr1      #SON OBJETOS VALOR
        self.expr2 = expr2

    def obtener_valor(self, actual, globa, ast):
        if(isinstance(self.expr1,Expresion) and isinstance(self.expr2,Expresion)):
            expr1 = self.expr1.obtener_valor(actual,globa,ast)
            expr2 = self.expr2.obtener_valor(actual,globa,ast)
            tipo_expr1 = self.expr1.tipo.obtener_tipo_dato()
            tipo_expr2 = self.expr2.tipo.obtener_tipo_dato()

            if(((tipo_expr1==TIPO.INT or tipo_expr1==TIPO.BIT or tipo_expr1==TIPO.DECIMAL)and(tipo_expr2==TIPO.INT or tipo_expr2==TIPO.BIT or tipo_expr2==TIPO.DECIMAL))):
                if((int(expr1)==0 or int(expr1)==1) and(int(expr2)==0 or int(expr2)==1)):
                    if((expr1 == 1) or expr2 == 1):
                        respuesta = VALOR(1,TIPO.BIT,self.linea,self.columna)   #1= VERDADERO
                    else:
                        respuesta = VALOR(0,TIPO.BIT,self.linea,self.columna)   #1= VERDADERO
                else:
                    respuesta = VALOR("ERROR",TIPO.ERROR,self.linea,self.columna)   #0= FALSO

            #EXTRA PORQUE NO SE ENTRA TAMBIEN
            elif((tipo_expr1 == TIPO.NCHAR or tipo_expr1 == TIPO.NVARCHAR)and (tipo_expr2 == TIPO.NCHAR or tipo_expr2 == TIPO.NVARCHAR)):
                if(expr1.lower() == "verdadero" and expr2.lower() == "verdadero"):
                    respuesta = VALOR(1,TIPO.BIT,self.linea,self.columna)
                elif (expr1.lower() == "verdadero" and expr2.lower() == "falso"):
                    respuesta = VALOR(1,TIPO.BIT,self.linea,self.columna)
                elif (expr1.lower() == "falso" and expr2.lower() == "verdadero"):
                    respuesta = VALOR(1,TIPO.BIT,self.linea,self.columna)
                elif (expr1.lower() == "falso" and expr2.lower() == "falso"):
                    respuesta = VALOR(0,TIPO.BIT,self.linea,self.columna)
                else:
                    respuesta = VALOR("ERROR",TIPO.ERROR,self.linea,self.columna)
            else:
                respuesta = VALOR("ERROR",TIPO.ERROR,self.linea,self.columna) 
            
        else:
            respuesta = VALOR("ERROR",TIPO.ERROR,self.linea,self.columna)
        #BORRAR
        ast.escribir_en_consola("LA RESPUESTA ES: "+str(respuesta.valor) +"\n")
        self.tipo = respuesta.tipo
        return respuesta.obtener_valor(actual,globa,ast)