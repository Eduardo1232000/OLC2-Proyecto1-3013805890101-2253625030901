from FUNCIONES.ARBOL.EJECUCION import *
from FUNCIONES.ARBOL.VALOR import *
from FUNCIONES.ERROR_LSS import *
from FUNCIONES.ARBOL.AST import *

import xml.etree.ElementTree as ET

class CONCATENAR(Expresion):        
    def __init__(self, cadena1,cadena2, linea, columna):
        super().__init__(linea, columna, "CONCATENAR")
        self.cadena1 = cadena1      #SON OBJETOS VALOR
        self.cadena2 = cadena2

    def obtener_valor(self, actual, globa, ast):
        #print(self.text)
        if(isinstance(self.cadena1,Expresion) and isinstance(self.cadena2,Expresion)):
            cadena1 = self.cadena1.obtener_valor(actual,globa,ast)
            cadena2 = self.cadena2.obtener_valor(actual,globa,ast)
            tipo_cadena1 = self.cadena1.tipo.obtener_tipo_dato()
            tipo_cadena2 = self.cadena2.tipo.obtener_tipo_dato()
            
            #VALIDACION DE TIPOS
            if(((self.cadena1.tipo.obtener_tipo_dato() == TIPO.NVARCHAR or self.cadena1.tipo.obtener_tipo_dato() == (TIPO.NCHAR)) and (self.cadena2.tipo.obtener_tipo_dato() == TIPO.NVARCHAR or self.cadena2.tipo.obtener_tipo_dato() == TIPO.NCHAR))):
                val_respuesta = cadena1 + cadena2
            elif(tipo_cadena1 == TIPO.COLUMNA or tipo_cadena1==TIPO.ALIAS or tipo_cadena2 == TIPO.COLUMNA or tipo_cadena2 == TIPO.ALIAS):
                print("SERA COLUMNA O ALIAS")
                
                #VALIDACION DE COLUMNAS
                nombre_base = ast.obtener_base_activa()
                nombre_tabla = ast.obtener_tabla_activa()
                #print(nombre_tabla)
                ruta = "BASE_DATOS/"+str(nombre_base)+".xml"
                obj_tabla = self.obtener_objeto_tabla(ruta,nombre_tabla)
                valor_exp1 = None
                valor_exp2 = None
                if(tipo_cadena1 == TIPO.COLUMNA and nombre_tabla != None):
                    valor_exp1 = self.obtener_lista_datos(obj_tabla,cadena1)
                elif(tipo_cadena1 == TIPO.ALIAS):
                    valor_exp1 = cadena1
                else:
                    valor_exp1 = cadena1
                if(tipo_cadena2 == TIPO.COLUMNA and nombre_tabla != None):
                    valor_exp2 = self.obtener_lista_datos(obj_tabla,cadena2)
                elif(tipo_cadena2 == TIPO.ALIAS):
                    valor_exp2 = cadena2
                else:
                    valor_exp2 = cadena2

                #print(cadena1)
                #print(valor_exp2)

                if((tipo_cadena1 == TIPO.COLUMNA or tipo_cadena1 == TIPO.ALIAS)  and (tipo_cadena2 == TIPO.COLUMNA or tipo_cadena2 == TIPO.ALIAS)):
                    lista_respuesta1 = []
                    lista_respuesta1.append(valor_exp1[0])
                    lista_respuesta1.append("CONCATENAR")
                    if(valor_exp1[0] == valor_exp2[0]):
                        lst_vals=[]
                        for i in range(len(valor_exp1[2])):
                            val = valor_exp1[2][i]
                            val2 = valor_exp2[2][i]
                            lst_vals.append(str(val)+str(val2))
                    else:
                        val = VALOR("",TIPO.ERROR,self.linea,self.columna)
                        self.tipo = val.tipo
                        return None

                    val = VALOR("",TIPO.LISTA_COLUMNAS,self.linea,self.columna)
                    self.tipo = val.tipo
                    lista_respuesta1.append(lst_vals)
                    return lista_respuesta1
                elif(tipo_cadena1 == TIPO.COLUMNA or tipo_cadena1 == TIPO.ALIAS):
                    lista_respuesta1 = []
                    lista_respuesta1.append(valor_exp1[0])
                    lista_respuesta1.append("CONCATENAR")
                    lst_vals = []
                    for i in range(len(valor_exp1[2])):
                        val = valor_exp1[2][i]
                        lst_vals.append(str(val)+str(valor_exp2))
                    lista_respuesta1.append(lst_vals)

                    val = VALOR("",TIPO.LISTA_COLUMNAS,self.linea,self.columna)
                    self.tipo = val.tipo
                    return lista_respuesta1
                
                elif(tipo_cadena2 == TIPO.COLUMNA or tipo_cadena2 == TIPO.ALIAS):
                    lista_respuesta1 = []
                    lista_respuesta1.append(valor_exp2[0])
                    lista_respuesta1.append("CONCATENAR")
                    lst_vals = []
                    for i in range(len(valor_exp2[2])):
                        val = valor_exp2[2][i]
                        lst_vals.append(str(valor_exp1)+str(val))

                    lista_respuesta1.append(lst_vals)
                    val = VALOR("",TIPO.LISTA_COLUMNAS,self.linea,self.columna)
                    self.tipo = val.tipo
                    print(lista_respuesta1)
                    return lista_respuesta1
                else:
                    print("ERROR INESPERADO EN IGUAL")
                
                
            else:
                ast.escribir_en_consola("ERROR: No se pudo reconocer el tipo de dato de los valores")
                ast.insertar_error_semantico(ERROR_LSS("SEMANTICO","CONCATENAR: No se pudo reconocer el tipo de dato de los valores",self.linea))
                respuesta = VALOR("ERROR",TIPO.ERROR,self.linea,self.columna)
                self.tipo = respuesta.tipo
                return "ERROR"

        #GENERAMOS OBJETO RESPUESTA CON DATOS QUE PIDE EL ENUNCIADO
        respuesta = VALOR(val_respuesta,TIPO.NVARCHAR,self.linea,self.columna)

        #BORRAR
        ast.escribir_en_consola("LA NUEVA CADENA ES: "+respuesta.valor +"\n")
        self.tipo = respuesta.tipo
        return val_respuesta
    

    def obtener_objeto_tabla(self,ruta,nomtabla):
        tree = ET.parse(ruta)
        root = tree.getroot()
        for base in root.findall('base'):
            for tabla in base.findall('tabla'):
                if(tabla.attrib['name'] == nomtabla):
                    return tabla
        return None
                
    def encontrar_campo(self, objeto_tabla, nomcampo):
        contador = -1
        for campos in objeto_tabla.findall('campo'):
            contador +=1
            if(campos[0].text == nomcampo):
                return contador
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