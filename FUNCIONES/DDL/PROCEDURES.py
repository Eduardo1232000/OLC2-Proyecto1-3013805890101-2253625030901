from FUNCIONES.ARBOL.EJECUCION import *
from FUNCIONES.ARBOL.VALOR import *
from FUNCIONES.CREAR_BASE import *
from FUNCIONES.ARBOL.TABLA_FUNCIONES_VARIABLES import *
from FUNCIONES.ARBOL.AST import *
from FUNCIONES.ERROR_LSS import *

from FUNCIONES.ARBOL.TABLA_FUNCIONES_VARIABLES import *

class CREATE_PROCEDURE(Instruccion):        
    def __init__(self,nombre,tipo_v,lista_variables,lista_instruccion, linea, columna):
        super().__init__(linea, columna, "CREATE PROCEDURE ")
   #SON OBJETOS VALOR
        self.nombre = nombre    #VALOR
        self.tipo = tipo_v      #STRING
        self.lista_variables = lista_variables #LISTA NOMBRES DE VARIABLES A GUARDAR
        self.lista_instruccion = lista_instruccion #LISTA DE OBJETOS INSTRUCCION O EXPRESION

    def ejecutar(self, actual, globa, ast):
        if(isinstance(actual,TABLA_FUNCIONES_Y_VARIABLES) and isinstance(globa,TABLA_FUNCIONES_Y_VARIABLES) and isinstance(ast, AST) and isinstance(self.nombre, Expresion)):
            nombre_func = self.nombre.obtener_valor(actual,globa,ast)
            lista_parametros = []
            for var in self.lista_variables:
                if(isinstance(var[0], Expresion) and isinstance(var[1],TIPODATO)):
                    nombre_variable = var[0].obtener_valor(actual,globa,ast)
                    if(var[1].tipo == TIPO.INT):
                        res = 0
                        tipo_var = "INT"
                    elif(var[1].tipo == TIPO.DECIMAL):
                        res = 0.0
                        tipo_var = "DECIMAL"
                    elif(var[1].tipo == TIPO.DATE):
                        res = ""
                        tipo_var = "DATE"
                    elif(var[1].tipo == TIPO.DATETIME):
                        res = ""
                        tipo_var = "DATETIME"
                    elif(var[1].tipo == TIPO.NCHAR):
                        res = ""
                        tipo_var = "NCHAR"
                    elif(var[1].tipo == TIPO.NVARCHAR):
                        res = ""
                        tipo_var = "NVARCHAR"
                    else:
                        res="ERROR"
                        tipo_var = "ERROR"
                    objeto_variable = VARIABLE(nombre_variable,tipo_var,res)
                    lista_parametros.append(objeto_variable)           

            objeto_procedure = PROCEDURE(nombre_func,lista_parametros,self.lista_instruccion)
            actual.agregar_procedure_tabla(nombre_func,objeto_procedure)

            #GUARDAR VARIABLES EN EL NUEVO AMBITO
            actual.agregar_procedure_tabla(nombre_func,objeto_procedure)
            ast.escribir_en_consola("PROCEDURE CREADO\n")

class EJECUTAR_PROCEDURE(Instruccion):
    def __init__(self,id,lista_valores, linea, columna):
        super().__init__(linea, columna, "EJECUTAR PROCEDURE")
        self.id = id
        self.lista_valores = lista_valores
    
    def ejecutar(self, actual, globa, ast):
        if(isinstance(actual,TABLA_FUNCIONES_Y_VARIABLES) and isinstance(globa,TABLA_FUNCIONES_Y_VARIABLES) and isinstance(ast, AST) and isinstance(self.id,Expresion)):
            nombre_procedure = self.id.obtener_valor(actual,globa,ast)
            objeto_procedure = actual.obtener_procedure(nombre_procedure)
            if(isinstance(objeto_procedure,PROCEDURE)):
                
                parametros_procedure = objeto_procedure.obtener_parametros()
                instrucciones_procedure = objeto_procedure.obtener_sentencias()

                #print(len(parametros_procedure))
                #print(len(self.lista_valores))

                #VALIDACION NUMERO DE VALORES COINCIDE CON NUMERO DE PARAMETROS
                if(len(parametros_procedure) != len(self.lista_valores)):
                    ast.escribir_en_consola("ERROR: El numero de parametros no coincide con el numero de variables del procedimiento")
                    return
                
                #CREAR EL AMBITO DE PROCEDURE
                ambito_procedure = TABLA_FUNCIONES_Y_VARIABLES(actual,nombre_procedure)
                for i in range(len(self.lista_valores)):
                    lista_valor_variable = self.lista_valores[i]
                    objeto_variable_guardar = lista_valor_variable[0]
                    objeto_valor_variable = lista_valor_variable[1]

                    if(isinstance(objeto_variable_guardar, Expresion) and isinstance(objeto_valor_variable, Expresion)):   #SI TIENE NOMBRES DE VARIABLES
                        variable_guardar = objeto_variable_guardar.obtener_valor(actual,globa,ast)
                        valor_variable = objeto_valor_variable.obtener_valor(actual,globa,ast)
                        #print(variable_guardar)
                        #print(valor_variable)

                        for j in range (len(parametros_procedure)):
                            var = parametros_procedure[j]
                            if(isinstance(var,VARIABLE)):

                                nombre_var = var.obtener_nombre()
                                if(nombre_var != variable_guardar): #SI NO ES EL MISMO NOMBRE PASA AL SIGUIENTE
                                    continue

                                #print("ENCONTRE")
                                tipo_var = var.obtener_tipo()
                                tipo_valor = objeto_valor_variable.tipo.obtener_tipo_dato()

                                #VALIDACION TIPOS
                                if(tipo_var != tipo_valor):
                                    ast.escribir_en_consola("ERROR: El valor "+str(valor_variable)+" no es del tipo correcto en el procedure\n")
                                    return 
                                
                                #VALIDAR QUE NO SE HAYA GUARDADO
                                validacion_existe = ambito_procedure.variable_existe(nombre_var)
                                if(validacion_existe == True):
                                    ast.escribir_en_consola("ERROR: La variable "+str(nombre_var)+"se inserto mas de 1 vez\n")
                                var.modificar_valor(valor_variable)
                                ambito_procedure.agregar_variable_tabla(var)

                    elif(isinstance(objeto_valor_variable,Expresion)):
                        
                        valor_variable = objeto_valor_variable.obtener_valor(actual,globa,ast)
                        #print(valor_variable)
    
                        var = parametros_procedure[i]
                        if(isinstance(var,VARIABLE)):
                            nombre_var = var.obtener_nombre()
                            tipo_var = var.obtener_tipo()
                            tipo_valor = objeto_valor_variable.tipo.obtener_tipo_dato()
                            #print(tipo_var)
                            #print(tipo_valor)

                            #VALIDACION TIPOS
                            if(tipo_var != tipo_valor):
                                if(tipo_var== TIPO.INT and tipo_valor == TIPO.BIT):
                                    pass
                                else:
                                    ast.escribir_en_consola("ERROR: El valor "+str(valor_variable)+" no es del tipo correcto en el procedure\n")
                                    return 
                            
                            var.modificar_valor(valor_variable)
                            ambito_procedure.agregar_variable_tabla(nombre_var,var)
                                       
                    else:
                        print("ERROR")

                #EJECUTAR CADA INSTRUCCION
                for instr in instrucciones_procedure[0]:
                    if isinstance(instr,Instruccion):
                        instr.ejecutar(ambito_procedure,globa,ast)

                    elif(isinstance(instr, Expresion)):                 #SI EN EL ARBOL APARECE UNA EXPRESION SOLO ASI, DA IGUAL EL VALOR PORQUE ASI SE HIZO EN EL IDE
                        instr.obtener_valor(ambito_procedure,globa,ast)     # ES DECIR QUE SOLO ESCRIBIERON 1+1 Y NO LO ASIGNARON A ALGUNA VARIABLE



