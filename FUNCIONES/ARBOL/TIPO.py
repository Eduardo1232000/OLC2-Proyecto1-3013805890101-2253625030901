class TIPO:
    INT = "INT"
    BIT = "BIT"
    DECIMAL = "DECIMAL"
    DATE = "DATE"
    DATETIME = "DATETIME"
    CHAR = "CHAR"
    VARCHAR = "VARCHAR"
    ERROR = "ERROR"

class TIPODATO:
    def __init__(self,tipo,size=0) -> None:
        self.tipo = tipo
        self.size = size

    def obtener_tipo_dato(self):
        return self.tipo
    
    def obtener_size(self):
        return self.size
    
    def modificar_size(self,valor):
        try:
            if(self.tipo == TIPO.CHAR):
                self.size = int(valor)
        except:
            print("EL VALOR NO ES UN NUMERO")