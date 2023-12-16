class NODO_TABLA_SIMBOLOS:
    def __init__(self,identificador,base, tipo_var_fun,tipo,dimension,entorno,referencia,linea,columna):
        self.identificador = identificador
        self.base = base
        self.tipo_var_fun = tipo_var_fun
        self.tipo = tipo 
        self.dimension = dimension
        self.entorno = entorno
        self.referencia = referencia
        self.linea = linea
        self.columna=columna

    def obtener_identificador(self):
        return self.identificador
    
    def obtener_base(self):
        return self.base

    def obtener_tipo_var_fun(self):
        return self.tipo_var_fun
    
    def obtener_tipo(self):
        return self.tipo
    
    def obtener_entorno(self):
        return self.entorno

    def obtener_linea(self):
        return self.linea
    
    def obtener_columna(self):
        return self.columna
    
    def obtener_dimension(self):
        return self.dimension
    
    def obtener_referencia(self):
        return self.referencia