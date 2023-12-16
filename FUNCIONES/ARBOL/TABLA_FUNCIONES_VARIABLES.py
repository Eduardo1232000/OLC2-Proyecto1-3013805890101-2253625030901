class TABLA_FUNCIONES_Y_VARIABLES:
    def __init__(self,anterior, nombre) :
        self.anterior = anterior  #AMBITO ANTERIOR (LISTA)
        self.tabla_variables = []   #ALMACENA LAS VARIABLES
        self.tabla_funciones = []   #ALMACENA LAS FUNCIONES
        self.tabla_procedimientos = [] #ALMACENA LOS PROCEDURES
        self.nombre = nombre        #EL NOMBRE DEL AMBITO (STRING)

    def agregar_variable_tabla(self,id,variable):    #id(STRING) variable(OBJETO VARIABLE)
        lst_temporal = []
        lst_temporal.append(id)
        lst_temporal.append(variable)
        self.tabla_variables.append(lst_temporal)
        
    def obtener_variable(self,id):              #ID(STRING) RETORNA OBJETO VARIABLE
        for lst in self.tabla_variables:
            if(lst[0] == str(id)):
                return(lst[1])
        return None
    
    def variable_existe(self,id):       #ID (STRING) RETORNA BOOL
        for lst in self.tabla_variables:
            if(lst[0] == id):
                return True
        return False
    
    def procedure_existe(self,id):
        for lst in self.tabla_procedimientos:
            if(lst[0] == id):
                return True
        return False
    
    def funcion_existe(self,id):
        for lst in self.tabla_funciones:
            if(lst[0] == id):
                return True
        return False
    
    def agregar_funcion_tabla(self,id,funcion): #ID (STRING) , FUNCION(OBJETO FUNCION)
        lst_temporal = []
        lst_temporal.append(id)
        lst_temporal.append(funcion)
        self.tabla_funciones.append(lst_temporal)   

    def obtener_funcion(self, id):  #ID(STRING)  RETORNA OBJETO FUNCION  
        for lst in self.tabla_funciones:
            if(str(lst[0]) == str(id)):
                return(lst[1])
        return None
    
    def agregar_procedure_tabla(self,id,funcion): #ID (STRING) , FUNCION(OBJETO FUNCION)
        lst_temporal = []
        lst_temporal.append(id)
        lst_temporal.append(funcion)
        self.tabla_procedimientos.append(lst_temporal)   

    def obtener_procedure(self, id):  #ID(STRING)  RETORNA OBJETO FUNCION  
        for lst in self.tabla_procedimientos:
            if(str(lst[0]) == str(id)):
                return(lst[1])
        return None
    
class VARIABLE:
    def __init__(self,id,tipo,size_tipo,valor):
        self.id = id
        self.tipo = tipo
        self.size_tipo = size_tipo
        self.valor = valor

    def obtener_valor(self):
        return (self.valor)
    
    def modificar_valor(self, valor):
        self.valor = valor

    def obtener_nombre(self):
        return self.id
    
    def obtener_tipo(self):
        return self.tipo
    
    def obtener_size_tipo(self):
        return self.size_tipo
    
class FUNCION:
    def __init__(self,nombre, tipo,size_tipo, parametros, sentencias):
        self.tipo = tipo        #(TIPO)
        self.nombre = nombre    #(STRING)
        self.size_tipo = size_tipo
        self.parametros = parametros #(LISTA)
        self.sentencias = sentencias #(LISTA)

    def obtener_nombre(self):
        return self.nombre
    
    def obtener_tipo(self):
        return self.tipo
        
    def obtener_parametros(self):
        return self.parametros
    
    def obtener_sentencias(self):
        return self.sentencias
    
class PROCEDURE:
    def __init__(self,nombre, parametros, sentencias):
        self.nombre = nombre    #(STRING)
        self.parametros = parametros #(LISTA)
        self.sentencias = sentencias #(LISTA)

    def obtener_nombre(self):
        return self.nombre
    
    def obtener_parametros(self):
        return self.parametros
    
    def obtener_sentencias(self):
        return self.sentencias