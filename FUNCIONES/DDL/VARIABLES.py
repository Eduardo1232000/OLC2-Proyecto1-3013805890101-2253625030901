from FUNCIONES.ARBOL.EJECUCION import *
from FUNCIONES.ARBOL.VALOR import *
from FUNCIONES.CREAR_BASE import *
from FUNCIONES.ARBOL.TABLA_FUNCIONES_VARIABLES import *
from FUNCIONES.ARBOL.AST import *
from FUNCIONES.ERROR_LSS import *

class DECLARE(Instruccion):        
    def __init__(self,nombre,tipo_v, linea, columna):
        super().__init__(linea, columna, "CREATE ")
   #SON OBJETOS VALOR
        self.nombre = nombre    #ES UN VALOR
        self.tipo = tipo_v


    def ejecutar(self, actual, globa, ast):
        if(isinstance(actual,TABLA_FUNCIONES_Y_VARIABLES) and isinstance(globa,TABLA_FUNCIONES_Y_VARIABLES) and isinstance(ast, AST) and isinstance(self.tipo,TIPODATO) and isinstance(self.nombre, VALOR)):
            #VALIDAR SI YA EXISTE
            id = self.nombre.obtener_valor(actual,globa,ast)
            if(actual.variable_existe(id)):     #SI EXISTE LA VARIABLE
                ast.escribir_en_consola("ERROR: Variable "+str(id)+" ya existe !\n")
                ast.insertar_error_semantico(ERROR_LSS("SEMANTICO","DECLARE: Variable "+str(id)+" ya existe",self.linea))
                return
            
            #RECONOCER EL TIPO DE LA VARIABLE
            if(self.tipo.tipo == TIPO.INT):
                res = 0
                tipo_valor_tabla_simbolo = "INT"
            elif(self.tipo.tipo == TIPO.DECIMAL):
                res = 0.0
                tipo_valor_tabla_simbolo = "DECIMAL"
            elif(self.tipo.tipo == TIPO.DATE):
                res = "01-01-1753"
                tipo_valor_tabla_simbolo = "DATE"
            elif(self.tipo.tipo == TIPO.DATETIME):
                res = "01-01-1753 10:10"
                tipo_valor_tabla_simbolo = "DATETIME"
            elif(self.tipo.tipo == TIPO.NCHAR):
                res = ""
                tipo_valor_tabla_simbolo = "NCHAR"
            elif(self.tipo.tipo == TIPO.NVARCHAR):
                res = ""
                tipo_valor_tabla_simbolo = "NVARCHAR"

            variable_crear = VARIABLE(id,tipo_valor_tabla_simbolo,self.tipo.obtener_size(),res)
            actual.agregar_variable_tabla(id,variable_crear)
            ast.guardar_en_tabla_simbolos(id,"VARIABLE","-", tipo_valor_tabla_simbolo,actual,self.linea,self.columna)
            ast.escribir_en_consola("Variable "+str(id) +" Creada!\n")
        #VALIDAR SI EXISTE EN EL AMBITO

class ASIGNAR_VARIABLE(Instruccion):
    def __init__(self,id,valor, linea, columna):
        super().__init__(linea, columna, "ASIGNACION VARIABLE")
        self.id = id
        self.valor = valor

    def ejecutar(self, actual, globa, ast):
        if(isinstance(actual,TABLA_FUNCIONES_Y_VARIABLES) and isinstance(globa,TABLA_FUNCIONES_Y_VARIABLES) and isinstance(ast, AST) and isinstance(self.id,Expresion)):
            id_var = self.id.obtener_valor(actual,globa,ast)
            validar_existe = actual.variable_existe(str(id_var))
            if(validar_existe == False):
                ast.escribir_en_consola("ERROR: La variable "+str(id_var)+" no existe!\n")
                ast.insertar_error_semantico(ERROR_LSS("SEMANTICO","DECLARE: La variable "+str(id_var)+" no existe!",self.linea))
                return
            
            objeto_variable = actual.obtener_variable(str(id_var))
            if(isinstance(objeto_variable,VARIABLE) and isinstance(self.valor,Expresion)):
                

                val = self.valor.obtener_valor(actual,globa,ast)
                #TRUNCAR TEXTO SI ES NCHAR
                if(objeto_variable.obtener_tipo() == "NCHAR"):
                    nuevo_val = ""
                    print(objeto_variable.obtener_size_tipo())
                    if(len(str(val))>int(objeto_variable.obtener_size_tipo())):
                        for i in range(int(objeto_variable.obtener_size_tipo())):
                            nuevo_val += str(val)[i]
                        objeto_variable.modificar_valor(nuevo_val)
                        ast.escribir_en_consola("VARIABLE MODIFICADA!\n")
                        return

                objeto_variable.modificar_valor(val)

                ast.escribir_en_consola("VARIABLE MODIFICADA!\n")
            

class VALIDAR_EXISTE_VARIABLE(Expresion):
    def __init__(self,id, linea, columna):
        super().__init__(linea, columna, "OBTENCION VARIABLE")
        self.id = id
    
    def obtener_valor(self, actual, globa, ast):
        if(isinstance(actual,TABLA_FUNCIONES_Y_VARIABLES) and isinstance(globa,TABLA_FUNCIONES_Y_VARIABLES) and isinstance(ast, AST)):
            id_var = self.id.obtener_valor(actual,globa,ast)
            validar_existe = actual.variable_existe(str(id_var))
            if(validar_existe == False):
                ast.escribir_en_consola("ERROR: La variable "+str(id_var)+" no existe!\n")
                ast.insertar_error_semantico(ERROR_LSS("SEMANTICO","DECLARE: Variable "+str(id_var)+" no existe",self.linea))
                val = VALOR("ERROR","ERROR",self.linea,self.columna)
                self.tipo = val.tipo
                return "ERROR"
            objeto_variable = actual.obtener_variable(str(id_var))
            if(isinstance(objeto_variable,VARIABLE)):
                valor_variable = objeto_variable.obtener_valor()
                #print(valor_variable)
                tipo_variable = objeto_variable.obtener_tipo()
                self.tipo = tipo_variable
                #print(self.tipo)
                val = VALOR(valor_variable,tipo_variable,self.linea,self.columna)
                self.tipo = val.tipo
                #print(valor_variable)
                return(valor_variable)
            else:
                val = VALOR("ERROR","ERROR",self.linea,self.columna)
                self.tipo = val.tipo
                return("ERROR")
        
        