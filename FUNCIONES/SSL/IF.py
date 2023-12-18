from FUNCIONES.ARBOL.EJECUCION import *
from FUNCIONES.ARBOL.VALOR import *
from FUNCIONES.ERROR_LSS import *
from FUNCIONES.ARBOL.TABLA_FUNCIONES_VARIABLES import *
from FUNCIONES.SSL.RETURN import *

class EXP_IF(Expresion):        
    def __init__(self,condicion, expr1,expr2, linea, columna):
        super().__init__(linea, columna, "IF")
        self.condicion = condicion
        self.expr1 = expr1      #SON OBJETOS VALOR
        self.expr2 = expr2

    def obtener_valor(self, actual, globa, ast):
        #print(self.text)
        if(isinstance(self.condicion,Expresion) and isinstance(self.expr1,Expresion) and isinstance(self.expr2,Expresion)):
            condicion = self.condicion.obtener_valor(actual,globa,ast)
            expr1 = self.expr1.obtener_valor(actual,globa,ast)
            expr2 = self.expr2.obtener_valor(actual,globa,ast)
            tipo_condicion = self.condicion.tipo.obtener_tipo_dato()
            tipo_expr1 = self.expr1.tipo.obtener_tipo_dato()
            tipo_expr2 = self.expr2.tipo.obtener_tipo_dato()

            if(tipo_condicion == TIPO.BIT or tipo_condicion == TIPO.INT):
                if(int(condicion) == 1 ):
                    respuesta = VALOR(expr1,tipo_expr1,self.linea, self.columna)
                elif(int(condicion) == 0):
                    respuesta = VALOR(expr2,tipo_expr2,self.linea, self.columna)
                else:
                    respuesta = VALOR("ERROR",TIPO.ERROR,self.linea, self.columna)
            else:
                respuesta = VALOR("ERROR",TIPO.ERROR,self.linea, self.columna)  
        else:
            respuesta = VALOR("ERROR",TIPO.ERROR,self.linea,self.columna)
        self.tipo = respuesta.tipo
        return respuesta.obtener_valor(actual,globa,ast)
    
class INS_IF(Instruccion):        
    def __init__(self,condicion,instrucciones_verdadero, instrucciones_falso, linea, columna):
        super().__init__(linea, columna, "IF")
        self.condicion = condicion                              #ES UN VALOR
        self.instrucciones_verdadero = instrucciones_verdadero  #LISTA INSTRUCCIONES
        self.instrucciones_falso = instrucciones_falso          #LISTA INSTRUCIONES

    def ejecutar(self, actual, globa, ast):
        #print(self.text)
        if(isinstance(self.condicion,Expresion)):
            condicion = self.condicion.obtener_valor(actual,globa,ast)
            print(condicion)
            tipo_condicion = self.condicion.tipo.obtener_tipo_dato()
            if(tipo_condicion == TIPO.INT or tipo_condicion == TIPO.BIT):
                #CREAMOS EL AMBITO DEL IF
                ambito_if = TABLA_FUNCIONES_Y_VARIABLES(actual,"IF")
                if(int(condicion) == 1): #EJECUTAR CONDICIONES VERDADERO
                    for instr in self.instrucciones_verdadero:
                        if(isinstance(instr,Instruccion)):
                            instr.ejecutar(ambito_if,globa,ast)
                            
                            if(isinstance(instr, RETURN) or (instr.ejecuto_return != None)):        #VALIDAR SI HAY RETURN
                                self.ejecuto_return = instr.ejecuto_return  #OBTENGO LO QUE RETORNA

                        elif(isinstance(instr,Expresion)):
                            instr.obtener_valor(ambito_if,globa,ast)

                elif(int(condicion) == 0):#EJECUTAR CONDICIONES FALSO
                    for instr in self.instrucciones_falso:
                        if(isinstance(instr,Instruccion)):
                            instr.ejecutar(ambito_if,globa,ast)

                            if(isinstance(instr, RETURN) or (instr.ejecuto_return != None)):    #VALIDAR SI HAY RETURN
                                self.ejecuto_return = instr.ejecuto_return  #OBTENGO LO QUE RETORNA
                                return  #NO SIGUE EJECUTANDO
                        elif(isinstance(instr,Expresion)):
                            instr.obtener_valor(ambito_if,globa,ast)
                else:#NO ES VALIDO
                    ast.escribir_en_consola("ERROR: La condicion no es de tipo BIT o INT (1 o 0)")
                    ast.insertar_error_semantico(ERROR_LSS("SEMANTICO","IF: La condicion no es de tipo BIT o INT (1 o 0)",self.linea))
                    return