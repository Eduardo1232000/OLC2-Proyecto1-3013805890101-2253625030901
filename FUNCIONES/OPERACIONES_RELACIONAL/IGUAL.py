from FUNCIONES.ARBOL.EJECUCION import *
from FUNCIONES.ARBOL.VALOR import *

class IGUAL(Expresion):        
    def __init__(self, expr1,expr2, linea, columna):
        super().__init__(linea, columna, "IGUAL")
        self.expr1 = expr1      #SON OBJETOS VALOR
        self.expr2 = expr2

    def obtener_valor(self, actual, globa, ast):
        if(isinstance(self.expr1,VALOR) and isinstance(self.expr2,VALOR)):
            expr1 = self.expr1.obtener_valor(actual,globa,ast)
            expr2 = self.expr2.obtener_valor(actual,globa,ast)
            tipo_expr1 = self.expr1.tipo.obtener_tipo_dato()
            tipo_expr2 = self.expr2.tipo.obtener_tipo_dato()
        
            if((tipo_expr1 == tipo_expr2) or ((tipo_expr1==TIPO.INT or tipo_expr1==TIPO.BIT or tipo_expr1==TIPO.DECIMAL)and(tipo_expr2==TIPO.INT or tipo_expr2==TIPO.BIT or tipo_expr2==TIPO.DECIMAL))):
                if(expr1 == expr2):
                    respuesta = VALOR(1,TIPO.BIT,self.linea,self.columna)   #1= VERDADERO
                else:
                    respuesta = VALOR(0,TIPO.BIT,self.linea,self.columna)   #0= FALSO
            else:
                respuesta = VALOR(0,TIPO.BIT,self.linea,self.columna)   #0= FALSO
            
        else:
            respuesta = VALOR("ERROR",TIPO.ERROR,self.linea,self.columna)
        #BORRAR
        ast.escribir_en_consola("LA RESPUESTA ES: "+str(respuesta.valor) +"\n")
        return respuesta