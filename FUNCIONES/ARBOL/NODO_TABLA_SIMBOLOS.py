class NODO_TABLA_SIMBOLOS:
    def __init__(self,identificador, tipo_var_fun,tipo,entorno,linea,columna):
        self.identificador = identificador
        self.tipo_var_fun = tipo_var_fun
        self.tipo = tipo 
        self.entorno = entorno
        self.linea = linea
        self.columna=columna

    def obtener_identificador(self):
        return self.identificador

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