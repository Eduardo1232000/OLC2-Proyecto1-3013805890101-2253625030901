from FUNCIONES.ARBOL.EJECUCION import *
from FUNCIONES.ARBOL.VALOR import *
from FUNCIONES.ERROR_LSS import *

class SUBSTRAER(Expresion):        
    def __init__(self, cadena1,inicio, final, linea, columna):
        super().__init__(linea, columna, "SUBSTRAER")
        self.cadena1 = cadena1      #SON OBJETOS VALOR (CADENA)
        self.inicio = inicio        #SON OBJETOS VALOR (INT)
        self.final = final          #SON OBJETOS VALOR (INT)

    def obtener_valor(self, actual, globa, ast):
        #print(self.text)
        if(isinstance(self.inicio,Expresion) and isinstance(self.final,Expresion) and isinstance(self.cadena1,Expresion)):
            num1 = self.inicio.obtener_valor(actual,globa,ast) - 1  #-1 porque en python el inicio es 0 y en el proyecto es 1
            num2 = self.final.obtener_valor(actual,globa,ast)
            cadena = self.cadena1.obtener_valor(actual,globa,ast)

            #tipo_inicio = self.inicio.tipo.obtener_tipo_dato()
            tipo_inicio = self.inicio.tipo.obtener_tipo_dato()
            tipo_final = self.final.tipo.obtener_tipo_dato()
            tipo_cadena = self.cadena1.tipo.obtener_tipo_dato()

            #SI INICIO Y FINAL SON ENTEROS O BIT(1 TAMBIEN ES ENTERO), Y CADENA ES NCHAR O NVARCHAR
            if((tipo_inicio == TIPO.INT or tipo_inicio == TIPO.BIT)and (tipo_final== TIPO.INT or tipo_final == TIPO.BIT)and (tipo_cadena == TIPO.NCHAR or tipo_cadena == TIPO.NVARCHAR) ):
                #EXTRA SI EL INICIO EN MENOR A 0 SE PONE POSICION 0
                
                if(num1<0):
                    num1 = 0
            
                val_respuesta = ""
                #VALIDACION SI EL NUMERO FINAL EXCEDE LA CANTIDAD DE CARACTERES 
                if(num2 > len(cadena)):
                    ast.escribir_en_consola("ERROR: El numero final, excede la cantidad de caracteres de la cadena!\n")
                    ast.insertar_error_semantico(ERROR_LSS("SEMANTICO","SUBSTRAER: El numero final excede la cantidad de caracteres de la cadena",self.linea))
                    respuesta = VALOR("ERROR",TIPO.ERROR,self.linea,self.columna)
                    self.tipo = respuesta.tipo
                    return "ERROR"
                for i in range (num1, num2):
                    val_respuesta += cadena[i]
                
                respuesta = VALOR(val_respuesta,TIPO.NVARCHAR,self.linea,self.columna)
                ast.escribir_en_consola("LA NUEVA CADENA ES: "+respuesta.valor +"\n")
                self.tipo = respuesta.tipo
                return val_respuesta
            else:
                ast.escribir_en_consola("ERROR: Expresiones de tipo incorrecto!\n")
                ast.insertar_error_semantico(ERROR_LSS("SEMANTICO","SUBSTRAER: Expresiones de tipo incorrecto",self.linea))