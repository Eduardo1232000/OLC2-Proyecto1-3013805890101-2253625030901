from FUNCIONES.ARBOL.EJECUCION import *
from FUNCIONES.ARBOL.VALOR import *
import xml.etree.ElementTree as ET

class EXP_NOT(Expresion):        
    def __init__(self, expr1, linea, columna):
        super().__init__(linea, columna, "NOT")
        self.expr1 = expr1      #SON OBJETOS VALOR

    def obtener_valor(self, actual, globa, ast):
        #print(self.text)
        if(isinstance(self.expr1,Expresion)):
            expr1 = self.expr1.obtener_valor(actual,globa,ast)
            tipo_expr1 = self.expr1.tipo.obtener_tipo_dato()




            if(tipo_expr1 == TIPO.LISTA_COLUMNAS ):
                #EN NOT SOLO VAMOS A RETORNAR LO CONTRARIO A LAS POSICIONES
                lst = []
                nombre_base = ast.obtener_base_activa()
                ruta = "BASE_DATOS/"+str(nombre_base)+".xml"
                lst_datos =[]
                for i in range(len(expr1)):
                    lst1 = expr1[i]
                    nombre_t = expr1[i][0]
                    #OBTENER LA LISTA DE DATOS DE LA TABLA
                    datos_t = expr1[i][2]
                    datos_ref = self.obtener_lista_datos(ruta,nombre_t)
                    for dato_ref in datos_ref:
                        if(dato_ref in datos_t):
                            pass
                        else:
                            lst_datos.append(dato_ref)                                      
                    expr1[i][2] = lst_datos
                val = VALOR("",TIPO.LISTA_COLUMNAS,self.linea,self.columna)
                self.tipo = val.tipo
                return expr1

            if(((tipo_expr1==TIPO.INT or tipo_expr1==TIPO.BIT or tipo_expr1==TIPO.DECIMAL))):
                if((int(expr1)==0 or int(expr1)==1)):
                    if(expr1 == 1):
                        respuesta = VALOR(0,TIPO.BIT,self.linea,self.columna)   #1= VERDADERO
                    else:
                        respuesta = VALOR(1,TIPO.BIT,self.linea,self.columna)   #1= VERDADERO
                else:
                    respuesta = VALOR("ERROR",TIPO.ERROR,self.linea,self.columna)   #0= FALSO

            #EXTRA PORQUE NO SE ENTRA TAMBIEN
            elif((tipo_expr1 == TIPO.NCHAR or tipo_expr1 == TIPO.NVARCHAR)):
                if(expr1.lower() == "verdadero"):
                    respuesta = VALOR(0,TIPO.BIT,self.linea,self.columna)
                elif (expr1.lower() == "falso"):
                    respuesta = VALOR(1,TIPO.BIT,self.linea,self.columna)
                else:
                    respuesta = VALOR("ERROR",TIPO.ERROR,self.linea,self.columna)
            else:
                respuesta = VALOR("ERROR",TIPO.ERROR,self.linea,self.columna) 
        else:
            respuesta = VALOR("ERROR",TIPO.ERROR,self.linea,self.columna)
        #BORRAR
        ast.escribir_en_consola("LA RESPUESTA ES: "+str(respuesta.valor) +"\n")
        self.tipo = respuesta.tipo
        return respuesta.obtener_valor(actual,globa,ast)
    
    def obtener_lista_datos(self,ruta,nombre_tabla):
        tree = ET.parse(ruta)
        root = tree.getroot()
        for base in root.findall('base'):
            for tabla in base.findall('tabla'):
                if(tabla.attrib['name'] == nombre_tabla):
                    lst = []
                    contador = -1
                    for dato in tabla.findall('dato'):
                        contador+=1
                        lst.append(contador)

                    return lst
        return None
    