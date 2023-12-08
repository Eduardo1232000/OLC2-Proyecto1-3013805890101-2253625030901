from FUNCIONES.ARBOL.EJECUCION import *
from FUNCIONES.ARBOL.TIPO import *
class VALOR(Expresion):
    def __init__(self,valor,tipo_valor, linea, columna):
        super().__init__(linea, columna, "VALOR")
        self.valor = valor
        self.tipo_valor = tipo_valor

    def obtener_valor(self, actual, globa, ast):
        try:
            if(self.tipo_valor == "INT"):
                self.tipo = TIPODATO(TIPO.INT)
                return(int(self.valor))

            elif(self.tipo_valor == "BIT"):
                self.tipo = TIPODATO(TIPO.BIT)
                return(int(self.valor))
            
            elif(self.tipo_valor == "DECIMAL"):
                self.tipo = TIPODATO(TIPO.DECIMAL)
                return(float(self.valor))

            elif(self.tipo_valor == "FECHA"):
                self.tipo = TIPODATO(TIPO.DATE)
                return(str(self.valor))

            elif(self.tipo_valor == "FECHAHORA"):
                self.tipo = TIPODATO(TIPO.DATETIME)
                return(str(self.valor))

            elif(self.tipo_valor == "CADENA"):
                self.tipo = TIPODATO(TIPO.VARCHAR)
                self.tipo.modificar_size(len(self.valor))  
                return str(self.valor)          
        except:
            print("NO SE PUEDE OBTENER EL VALOR DE LA EXPRESION")