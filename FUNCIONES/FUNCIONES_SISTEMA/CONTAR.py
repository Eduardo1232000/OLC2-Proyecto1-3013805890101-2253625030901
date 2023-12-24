from FUNCIONES.ARBOL.EJECUCION import *
from FUNCIONES.ARBOL.VALOR import *
from FUNCIONES.ARBOL.AST import *
import xml.etree.ElementTree as ET
import os

class CONTAR(Expresion):        
    def __init__(self, linea, columna):
        super().__init__(linea, columna, "CONTAR")
        self.validaciones_where = None
        self.cuenta = 0
        self.numero_campo = -1
        self.validaciones_where = None  
        val = VALOR("",TIPO.VALOR_UNICO,linea,columna)
        self.tipo = val.tipo  
         
    def obtener_valor(self, actual, globa, ast):         
        if(isinstance(ast,AST) ):
            tabla_activa = ast.obtener_tabla_activa()
            base_activa = ast.obtener_base_activa()
            ruta = "BASE_DATOS/"+str(base_activa)+".xml"

            obj_tabla = self.obtener_objeto_tabla(ruta,tabla_activa)

            if(obj_tabla != None):
                suma = 0

                #VALIDAR SI TIENE WHERE
                contador = -1
                if(self.validaciones_where != None):
                    valores_ref = None
                    for i in range(len(self.validaciones_where)):
                        tabla_ref = self.validaciones_where[i][0]
                        if(tabla_ref == tabla_activa):
                            print("ENCONTRE TABLA")
                            valores_ref = self.validaciones_where[i][2]

                    if(valores_ref != None):
                        #print(valores_ref)
                        
                        for dato in obj_tabla.findall('dato'):
                            contador +=1
                            try:
                                if contador in valores_ref:
                                    suma +=1
                            except:
                                suma = suma
                    else:
                        
                        for dato in obj_tabla.findall('dato'):
                            contador +=1
                            try:
                                suma +=1
                            except:
                                suma = suma

                else:
                    for dato in obj_tabla.findall('dato'):
                        try:
                            suma +=1
                        except:
                            suma = suma

            return suma
        

    def obtener_objeto_tabla(self,ruta,nomtabla):
        tree = ET.parse(ruta)
        root = tree.getroot()
        for base in root.findall('base'):
            for tabla in base.findall('tabla'):
                if(tabla.attrib['name'] == nomtabla):
                    return tabla
        return None
                    
    def obtener_lista_datos(self,objeto_tabla,nomcampo):
        lst_res = []
        lst_prin = []
        lst_prin.append(objeto_tabla.attrib['name'])
        lst_prin.append(nomcampo)
        contador =-1
        val = False
        for campos in objeto_tabla.findall('campo'):
            contador +=1
            if(campos[0].text == nomcampo):
                val = True
                break
        if(val == True):
            for dato in objeto_tabla.findall('dato'):
                lst_res.append(dato[contador].text)
        else:
            return None
        lst_prin.append(lst_res)
        return lst_prin             #[nombre_tabla, nombre_campo ,[valor,valor]]