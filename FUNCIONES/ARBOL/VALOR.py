from FUNCIONES.ARBOL.EJECUCION import *
from FUNCIONES.ARBOL.TIPO import *
class VALOR(Expresion):
    def __init__(self,valor,tipo_valor, linea, columna):
        super().__init__(linea, columna, "VALOR")
        self.text = ""
        self.valor = valor
        #print(valor)
        self.tipo_valor = tipo_valor
        if(self.tipo_valor == "INT"):
            if(self.valor == 0 or self.valor == 1):
                self.tipo = TIPODATO(TIPO.BIT)
            else:
                self.tipo = TIPODATO(TIPO.INT)

        elif(self.tipo_valor == "BIT"):
            self.tipo = TIPODATO(TIPO.BIT)  

        elif(self.tipo_valor == "DECIMAL"):
            self.tipo = TIPODATO(TIPO.DECIMAL)

        elif(self.tipo_valor == "FECHA"):
            self.tipo = TIPODATO(TIPO.DATE)

        elif(self.tipo_valor == "FECHAHORA"):
            self.tipo = TIPODATO(TIPO.DATETIME)

        elif(self.tipo_valor == "CADENA"):
            self.tipo = TIPODATO(TIPO.NVARCHAR)
            self.tipo.modificar_size(len(self.valor))  

        elif(self.tipo_valor == "NCHAR"):   
            self.tipo = TIPODATO(TIPO.NCHAR)

        elif(self.tipo_valor == "NVARCHAR"):   
            self.tipo = TIPODATO(TIPO.NVARCHAR)
            
        elif(self.tipo_valor == "ASTERISCO"):
            self.tipo = TIPODATO(TIPO.ASTERISCO)
            
        elif(self.tipo_valor == "COLUMNA"):
            self.tipo = TIPODATO(TIPO.COLUMNA)

        elif(self.tipo_valor == "ALIAS"):
            self.tipo = TIPODATO(TIPO.ALIAS)

        elif(self.tipo_valor == "LISTA_COLUMNAS"):
            self.tipo = TIPODATO(TIPO.LISTA_COLUMNAS) 

        elif(self.tipo_valor == "EXPRESION_SELECT"):
            self.tipo = TIPODATO(TIPO.LISTA_COLUMNAS)

        elif(self.tipo_valor == "VALOR_UNICO"):
            self.tipo = TIPODATO(TIPO.VALOR_UNICO)
            
        else:
            self.tipo = TIPODATO(TIPO.ERROR)

    def obtener_valor(self, actual, globa, ast):
        #print("SOY VALOR")
        try:
            #print(self.tipo_valor)
            if(self.tipo.obtener_tipo_dato() == TIPO.INT):
                return(int(self.valor))

            elif(self.tipo.obtener_tipo_dato() ==TIPO.BIT):
                return(int(self.valor))
            
            elif(self.tipo.obtener_tipo_dato() ==TIPO.DECIMAL):
                return(float(self.valor))

            elif(self.tipo.obtener_tipo_dato() ==TIPO.DATE):
                return(str(self.valor))

            elif(self.tipo.obtener_tipo_dato() ==TIPO.DATETIME):
                return(str(self.valor))

            elif(self.tipo.obtener_tipo_dato() ==TIPO.NVARCHAR):
                return str(self.valor) 
            
            elif(self.tipo.obtener_tipo_dato() ==TIPO.NCHAR):
                return str(self.valor)  
            
            elif(self.tipo.obtener_tipo_dato() ==TIPO.COLUMNA):
                return str(self.valor)
            
            elif(self.tipo.obtener_tipo_dato() ==TIPO.ALIAS):
                return self.valor
              
            elif(self.tipo.obtener_tipo_dato() ==TIPO.ASTERISCO):
                return "*"  
            
            elif(self.tipo.obtener_tipo_dato() ==TIPO.LISTA_COLUMNAS):
                return self.valor
            
            elif(self.tipo.obtener_tipo_dato()== TIPO.EXPRESION_SELECT):
                return self.valor
            
            elif(self.tipo.obtener_tipo_dato()== TIPO.VALOR_UNICO):
                return self.valor
                
        except:
            print("NO SE PUEDE OBTENER EL VALOR DE LA EXPRESION")

class FORANEA(Expresion):
    def __init__(self,base_origen,nombre_tabla,referencia, linea, columna):
        super().__init__(linea, columna, "FORANEA")
        self.base_origen = base_origen
        self.nombre_tabla = nombre_tabla
        self.referencia = referencia
        
    def obtener_base_origen(self):
        return(self.base_origen)
        
    def obtener_tabla_referencia(self):
        return(self.referencia)
    
    def obtener_tabla_base(self):
        return(self.nombre_tabla)
    
    def obtener_valor(self, actual, globa, ast):
        return(self.nombre_tabla)
        
class CAMPO_TABLA(Expresion):
    def __init__(self,nombre_tabla,tipo,nulo,primary_key,foreign_key,reference,linea,columna):
        super().__init__(linea, columna, "TABLA")
        self.nombre = nombre_tabla
        self.tipo = tipo
        self.nulo = nulo
        self.primary_key = primary_key
        self.foreign_key = foreign_key
        self.reference = reference

    def cambiar_nombre(self,valor):
        self.nombre = valor
    def cambiar_tipo(self,tipo):
        self.tipo = tipo

    def cambiar_nulo(self,valor):
        self.nulo = valor

    def cambiar_primary_key(self,valor):
        self.primary_key = valor

    def cambiar_foreign_key(self,valor):
        self.foreign_key = valor

    def cambiar_reference(self,valor):
        self.reference = valor

    def obtener_valor(self, actual, globa, ast):
        return self.nombre
    
    def obtener_tipo(self):
        return self.tipo 

    def obtener_nulo(self):
        return self.nulo 

    def obtener_primary_key(self):
        return self.primary_key
    
    def obtener_foreign_key(self):
        return self.foreign_key

    def obtener_reference(self):
        return self.reference
    