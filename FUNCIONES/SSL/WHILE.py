from FUNCIONES.ARBOL.EJECUCION import *
from FUNCIONES.ARBOL.VALOR import *
from FUNCIONES.ERROR_LSS import *
from FUNCIONES.ARBOL.TABLA_FUNCIONES_VARIABLES import *
from FUNCIONES.SSL.RETURN import *
    
class INS_WHILE(Instruccion):        
    def __init__(self,condicion,instrucciones_while, linea, columna):
        super().__init__(linea, columna, "WHILE")
        self.condicion = condicion    #ES UN VALOR
        self.instrucciones_while = instrucciones_while  #LISTA INSTRUCCIONES

    def ejecutar(self, actual, globa, ast):
        #print(self.text)
        if(isinstance(self.condicion,Expresion)):
            condicion = self.condicion.obtener_valor(actual,globa,ast)
            tipo_condicion = self.condicion.tipo.obtener_tipo_dato()

            if(tipo_condicion == TIPO.INT or tipo_condicion == TIPO.BIT):
                #CREAMOS EL AMBITO DEL IF
                while(self.condicion.obtener_valor(actual,globa,ast) == 1):    #SE EJECUTA SOLO SI LA CONDICION ES VERDADERA
                    ambito_while = TABLA_FUNCIONES_Y_VARIABLES(actual,"WHILE")  #NUEVA ITERACION = NUEVO AMBITO
                    for instr in self.instrucciones_while: #EJECUTAR CONDICIONES VERDADERO
                        if(isinstance(instr,Instruccion)):
                            instr.ejecutar(ambito_while,globa,ast) 
                            if(isinstance(instr, RETURN) or (instr.ejecuto_return != None)): #VALIDAR SI HAY RETURN
                                self.ejecuto_return = instr.ejecuto_return  #OBTENGO LO QUE RETORNA
                                return  #NO SIGO EJECUTANDO
                        elif(isinstance(instr,Expresion)):
                            instr.obtener_valor(ambito_while,globa,ast)
                return  #SOLO PARA ASEGURARNOS DE QUE FINALIZA
            else:
                ast.escribir_en_consola("("+str(self.linea)+")"+"ERROR: La condicion no es de tipo BIT o INT (1 o 0)")
                ast.insertar_error_semantico(ERROR_LSS("SEMANTICO","WHILE: La condicion no es de tipo BIT o INT (1 o 0)",self.linea))
                return