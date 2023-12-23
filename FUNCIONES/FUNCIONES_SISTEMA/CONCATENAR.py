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
            
            #VALIDACION DE TIPOS
            if(((self.cadena1.tipo.obtener_tipo_dato() == TIPO.NVARCHAR or self.cadena1.tipo.obtener_tipo_dato() == (TIPO.NCHAR)) and (self.cadena2.tipo.obtener_tipo_dato() == TIPO.NVARCHAR or self.cadena2.tipo.obtener_tipo_dato() == TIPO.NCHAR))):
                val_respuesta = cadena1 + cadena2
            elif(self.cadena1.tipo.obtener_tipo_dato() == TIPO.COLUMNA or self.cadena2.tipo.obtener_tipo_dato() == TIPO.COLUMNA):
                #VALIDAR EN LA TABLA
                if(isinstance(ast,AST)):
                    base_activa = ast.obtener_base_activa()
                    ruta = "BASE_DATOS/"+str(base_activa)+".xml"
                    tabla_activa = ast.obtener_tabla_activa()
                    tipo1 = self.cadena1.tipo.obtener_tipo_dato()
                    tipo2 = self.cadena2.tipo.obtener_tipo_dato()
                    if(tabla_activa == None):
                        ast.escribir_en_consola("ERROR: Se escribio un nombre de columna fuera del SELECT!")
                        ast.insertar_error_semantico(ERROR_LSS("SEMANTICO","CONCATENAR: Se escribio un nombre de columna fuera del SELECT!",self.linea))
                        respuesta = VALOR("ERROR",TIPO.ERROR,self.linea,self.columna)
                        self.tipo = respuesta.tipo
                        return "ERROR"
                    else:
                        obj_tabla = self.obtener_objeto_tabla(ruta,tabla_activa)
                        if(obj_tabla !=None):
                            val1=None
                            val2=None
                            salida = []
                            if(tipo1 == TIPO.COLUMNA):
                                val1 = self.cadena.obtener_valor(actual,globa,ast)
                                val1 = self.encontrar_campo(obj_tabla,self.cadena1)

                            if(tipo2 == TIPO.COLUMNA):
                                val2 = self.cadena.obtener_valor(actual,globa,ast)
                                val2 = self.encontrar_campo(obj_tabla,self.cadena2)

                            for datos in obj_tabla.findall('dato'):
                                if(tipo1 == TIPO.COLUMNA):
                                    valor1 = datos[val1].text
                                else:
                                    valor1 = cadena1
                                if(tipo2 == TIPO.COLUMNA):
                                    valor2 = datos[val2].text
                                else:
                                    valor2 = cadena2
                                salida.append(str(valor1)+str(valor2))

                            print(salida)
                            return salida


                    #HACER LA BUSQUEDA DE LA TABLA EN LA BASE Y ESPERAR
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