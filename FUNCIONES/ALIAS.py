from FUNCIONES.ARBOL.EJECUCION import *
from FUNCIONES.ARBOL.VALOR import *
from FUNCIONES.ERROR_LSS import *
from FUNCIONES.ARBOL.AST import *

import xml.etree.ElementTree as ET
import xml.dom.minidom

class ALIAS(Expresion):        
    def __init__(self, nombre_tabla,nombre_columna, linea, columna):
        super().__init__(linea, columna, "ALIAS")
        self.nombre_tabla = nombre_tabla      #SON OBJETOS VALOR
        self.nombre_columna = nombre_columna

    def obtener_valor(self, actual, globa, ast):
        if(isinstance(ast,AST) and isinstance(self.nombre_tabla,VALOR) and isinstance(self.nombre_columna,VALOR)):
            nom_tabla = self.nombre_tabla.obtener_valor(actual,globa,ast)
            nom_columna = self.nombre_columna.obtener_valor(actual,globa,ast)
            self.nombre_tabla = nom_tabla
            self.nombre_columna = nom_columna
            base_activa = ast.obtener_base_activa()

            ruta ="BASE_DATOS/"+str(base_activa)+".xml"
            tree = ET.parse(ruta)
            root = tree.getroot()

            tabla_existe = False

            for base in root.findall('base'):
                for tabla in base.findall('tabla'):
                    nombre = str(tabla.attrib['name'])
                    if nombre == nom_tabla:
                        tabla_existe = True
                        col_existe = False
                        contador = -1

                        lst = []
                        lst.append(nom_tabla)
                        lst.append(nom_columna)
                        for columnas in tabla.findall('campo'):
                            contador +=1
                            if(columnas[0].text == nom_columna):
                                validacion_col = True
                                respuesta = VALOR(contador,TIPO.ALIAS,self.linea,self.columna)
                                self.tipo = respuesta.tipo
                                col_existe = True
                                break
                        if(col_existe == True):
                            lst_dato = []
                            for datos in tabla.findall('dato'):
                                lst_dato.append(datos[contador].text)
                            lst.append(lst_dato)
                            return lst

                    #SI SALE AQUI ES PORQUE YA ENCONTRO LA TABLA Y NO LA COLUMNA (YA NO BUSCA EN EL RESTO DE TABLAS)
                    if(tabla_existe == True):
                        respuesta = VALOR(None,TIPO.ALIAS,self.linea,self.columna)
                        self.tipo = respuesta.tipo
                        return None
                            
        respuesta = VALOR(None,TIPO.ALIAS,self.linea,self.columna)
        self.tipo = respuesta.tipo
        return None