class TIPO:
    INT = "INT"
    BIT = "BIT"
    DECIMAL = "DECIMAL"
    DATE = "DATE"
    DATETIME = "DATETIME"
    NCHAR = "NCHAR"
    NVARCHAR = "NVARCHAR"
    ERROR = "ERROR"

    NULL = "NULL"
    NOT_NULL = "NOT NULL"
    PRIMARY_KEY = "PRIMARY KEY"

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
            if(self.tipo == TIPO.NCHAR):
                self.size = int(valor)
        except:
            print("EL VALOR NO ES UN NUMERO")