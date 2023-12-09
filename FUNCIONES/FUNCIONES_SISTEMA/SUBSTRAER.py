from FUNCIONES.ARBOL.EJECUCION import *
from FUNCIONES.ARBOL.VALOR import *

class SUBSTRAER(Expresion):        
    def __init__(self, cadena1,inicio, final, linea, columna):
        super().__init__(linea, columna, "SUBSTRAER")
        self.cadena1 = cadena1      #SON OBJETOS VALOR (CADENA)
        self.inicio = inicio        #SON OBJETOS VALOR (INT)
        self.final = final          #SON OBJETOS VALOR (INT)

    def obtener_valor(self, actual, globa, ast):
        if(isinstance(self.inicio,VALOR) and isinstance(self.final,VALOR) and isinstance(self.cadena1,VALOR)):
            num1 = self.inicio.obtener_valor(actual,globa,ast) - 1  #-1 porque en python el inicio es 0 y en el proyecto es 1
            num2 = self.final.obtener_valor(actual,globa,ast)
            cadena = self.cadena1.obtener_valor(actual,globa,ast)

            #tipo_inicio = self.inicio.tipo.obtener_tipo_dato()
            tipo_inicio = self.inicio.tipo.obtener_tipo_dato()
            tipo_final = self.final.tipo.obtener_tipo_dato()
            tipo_cadena = self.cadena1.tipo.obtener_tipo_dato()

            #SI INICIO Y FINAL SON ENTEROS O BIT(1 TAMBIEN ES ENTERO), Y CADENA ES CHAR O VARCHAR
            if((tipo_inicio == TIPO.INT or tipo_inicio == TIPO.BIT)and (tipo_final== TIPO.INT or tipo_final == TIPO.BIT)and (tipo_cadena == TIPO.CHAR or tipo_cadena == TIPO.VARCHAR) ):
                #EXTRA SI EL INICIO EN MENOR A 0 SE PONE POSICION 0
                
                if(num1<0):
                    num1 = 0
            
                val_respuesta = ""
                #VALIDACION SI EL NUMERO FINAL EXCEDE LA CANTIDAD DE CARACTERES 
                if(num2 > len(cadena)):
                    ast.escribir_en_consola("ERROR: El numero final, excede la cantidad de caracteres de la cadena!\n")
                    respuesta = VALOR("",TIPO.ERROR,self.linea,self.columna)
                    return respuesta
                for i in range (num1, num2):
                    val_respuesta += cadena[i]
                
                respuesta = VALOR(val_respuesta,TIPO.VARCHAR,self.linea,self.columna)
                ast.escribir_en_consola("LA NUEVA CADENA ES: "+respuesta.valor +"\n")
                return respuesta