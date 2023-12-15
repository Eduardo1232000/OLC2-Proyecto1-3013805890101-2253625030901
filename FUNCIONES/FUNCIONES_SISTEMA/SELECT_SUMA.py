from FUNCIONES.ARBOL.EJECUCION import *
from FUNCIONES.ARBOL.VALOR import *
from FUNCIONES.ARBOL.AST import *
import xml.etree.ElementTree as ET
import os

class SELECT_SUMA(Expresion):        
    def __init__(self, tabla_contar,tabla_ref, campo_ref, operacion, expresion, linea, columna):
        super().__init__(linea, columna, "SELECT SUMA")
        self.tabla_contar = tabla_contar
        self.campo_ref = campo_ref
        self.operacion = operacion
        self.expresion = expresion
        self.tabla_ref = tabla_ref

        self.cuenta = 0
        self.numero_campo = -1
        self.numero_campo_sumas =-1

        self.numero_campo_final = -1
        self.numero_campo_sumas_final = -1

        self.tipo = ""
        self.tipo_sumar = ""

    def operar(self, valor1, valor2, operacion):
        try:
            if(operacion == "="):
                if(str(valor1) == str(valor2)):
                    return True
                else:
                    return False
            elif(operacion == "!="):
                if(str(valor1) != str(valor2)):
                    return True
                else:
                    return False
            elif(operacion == "<"):
                if(int(valor1) < int(valor2)):
                    return True
                else:
                    return False
            elif(operacion == ">"):
                if(int(valor1) > int(valor2)):
                    return True
                else:
                    return False 
            elif(operacion == "<="):
                if(int(valor1) <= int(valor2)):
                    return True
                else:
                    return False 
            elif(operacion == ">="):
                if(int(valor1) >= int(valor2)):
                    return True
                else:
                    return False
        except:
            return False

    def obtener_valor(self, actual, globa, ast):
        operacion = self.operacion
        if(isinstance(self.expresion, Expresion) and isinstance(self.campo_ref,Expresion) and isinstance(ast,AST) and isinstance(self.tabla_ref,Expresion) and isinstance(self.tabla_contar,Expresion)):
            valor2 = self.expresion.obtener_valor(actual,globa,ast)
            valor_campo_ref = self.campo_ref.obtener_valor(actual,globa,ast)
            valor_tabla_ref = self.tabla_ref.obtener_valor(actual,globa,ast)
            nombre_base = ast.obtener_base_activa()

            valor_tabla_contar = self.tabla_contar.obtener_valor(actual,globa,ast)
            #BUSCAR LA TABLA EN LA BASE
            #CUENTA TODOS
            ruta = "BASE_DATOS/"+str(nombre_base)+".xml"
            tree = ET.parse(ruta)
            root = tree.getroot()
            base_existente = None
            campo_existente = None
            campo_valor_existente = None

            if os.path.exists(ruta):
                pass
            else:   #SI NO EXISTE LA BASE DE DATOS
                ast.escribir_en_consola("ERROR: No existe la base de datos : "+str(nombre_base)+"\n")
                ast.insertar_error_semantico(ERROR_LSS("SEMANTICO","SELECT: No existe la base de datos",self.linea))
                salida = VALOR("ERROR",TIPO.ERROR,self.linea,self.columna)
                self.tipo = salida.tipo
                return "ERROR"

            for base in root.findall('base'):                                   #RECORRE BASE
                if base.attrib['name'] == nombre_base:
                    for tabla in base:                                          #RECORRE TABLA
                        if tabla.attrib['name'] == valor_tabla_ref:
                            #VALIDAR EXISTE EL CAMPO
                            #VALIDAR EXISTE CAMPO OBTIENE LA POSICION
                            for campos in tabla.findall('campo'):               #RECORRE CAMPOS
                                #GUARDAR EL TIPO Y VALIDARLO DESPUES
                                for campo in campos.findall('nombre'):          #RECORRE PARAMETROS
                                    self.numero_campo = self.numero_campo+1

                                    if(campo.text == valor_campo_ref):
                                        campo_existente = campo
                                        self.numero_campo_final = self.numero_campo
                                    if(campo.text == valor_tabla_contar):
                                        campo_valor_existente = campo
                                        self.numero_campo_sumas_final = self.numero_campo
                                if(campo_existente is not None and campo_valor_existente is not None):
                                    break
                            #VALIDACION TIPO CAMPO A SUMAR SEA NUMERICO 
                            self.tipo = tabla[self.numero_campo_sumas_final]
                            self.tipo = self.tipo[1]
                            #print(self.tipo.text)
                            if(self.tipo.text == "BIT" or self.tipo.text == "INT" or self.tipo.text == "DECIMAL" ):
                                pass
                            else:
                                ast.escribir_en_consola("ERROR: El campo "+str(valor_tabla_contar)+" no es numerico\n")
                                ast.insertar_error_semantico(ERROR_LSS("SEMANTICO","SELECT: El campo "+str(valor_tabla_contar)+" no es numerico",self.linea))
                                salida = VALOR("ERROR",TIPO.ERROR,self.linea,self.columna)
                                self.tipo = salida.tipo
                                return "ERROR"
                                
                            #VALIDACION OBTUVO POSICION DE DATOS
                            if(campo_existente is None):
                                ast.escribir_en_consola("ERROR: El campo "+str(valor_campo_ref)+" no existe en la tabla\n")
                                ast.insertar_error_semantico(ERROR_LSS("SEMANTICO","SELECT: El campo "+str(valor_campo_ref)+" no existe en la tabla",self.linea))
                                salida = VALOR("ERROR",TIPO.ERROR,self.linea,self.columna)
                                self.tipo = salida.tipo
                                return "ERROR"
                            
                            if(campo_valor_existente is None):
                                ast.escribir_en_consola("ERROR: El campo "+str(valor_tabla_contar)+" no existe en la tabla\n")
                                ast.insertar_error_semantico(ERROR_LSS("SEMANTICO","SELECT: El campo "+str(valor_tabla_contar)+" no existe en la tabla",self.linea))
                                salida = VALOR("ERROR",TIPO.ERROR,self.linea,self.columna)
                                self.tipo = salida.tipo
                                return "ERROR"


                            #RECORRER LOS VALORES
                            #print(self.numero_campo)
                            for valores in tabla.findall('dato'):
                                valor1 = valores[self.numero_campo_final].text
                                valor1_sum = valores[self.numero_campo_sumas_final].text
                                if(valor1 is not None):
                                    res = self.operar(valor1,valor2,self.operacion)
                                    if res == True:
                                        try:
                                            self.cuenta = self.cuenta + int(valor1_sum)
                                        except:
                                            self.cuenta = self.cuenta
                            base_existente = tabla
                            break
                    if base_existente is not None:
                        break
        if(base_existente is None):
            ast.escribir_en_consola("ERROR: La TABLA "+str(valor_tabla_ref)+" No existe en la base !\n")
            ast.insertar_error_semantico(ERROR_LSS("SEMANTICO","SELECT: La tabla "+str(valor_tabla_ref)+" no existe en la base",self.linea))
            salida = VALOR("ERROR",TIPO.ERROR,self.linea,self.columna)
            self.tipo = salida.tipo
            return "ERROR"

        respuesta = self.cuenta
        #GENERAMOS OBJETO RESPUESTA CON DATOS QUE PIDE EL ENUNCIADO

        if(isinstance(self.cuenta,int)):
            salida = VALOR(respuesta,TIPO.INT,self.linea,self.columna)
        else:
            salida = VALOR(respuesta,TIPO.DECIMAL,self.linea,self.columna)
                    
        #BORRAR
        ast.escribir_en_consola("CONTAR:"+str(self.cuenta)+" \n")
        self.tipo = salida.tipo
        return respuesta