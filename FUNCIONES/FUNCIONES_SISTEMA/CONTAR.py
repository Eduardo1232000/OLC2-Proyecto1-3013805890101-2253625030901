from FUNCIONES.ARBOL.EJECUCION import *
from FUNCIONES.ARBOL.VALOR import *
from FUNCIONES.ARBOL.AST import *
import xml.etree.ElementTree as ET
import os

class CONTAR(Expresion):        
    def __init__(self, tabla_contar,tabla_ref, campo_ref, operacion, expresion, linea, columna):
        super().__init__(linea, columna, "CONTAR")
        self.tabla_contar = tabla_contar
        self.campo_ref = campo_ref
        self.operacion = operacion
        self.expresion = expresion
        self.tabla_ref = tabla_ref

        self.cuenta = 0
        self.numero_campo = -1
        
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
        #print(self.text)
        operacion = self.operacion
           
            
        if(isinstance(self.expresion, Expresion) and isinstance(self.campo_ref,Expresion) and isinstance(ast,AST) and isinstance(self.tabla_ref,Expresion)):
            valor2 = self.expresion.obtener_valor(actual,globa,ast)
            valor_campo_ref = self.campo_ref.obtener_valor(actual,globa,ast)
            valor_tabla_ref = self.tabla_ref.obtener_valor(actual,globa,ast)
            nombre_base = ast.obtener_base_activa()
            if(isinstance(self.tabla_contar,Expresion)):
                valor_tabla_contar = self.tabla_contar.obtener_valor(actual,globa,ast)
                #BUSCAR LA TABLA EN LA BASE

            else:
                #CUENTA TODOS
                ruta = "BASE_DATOS/"+str(nombre_base)+".xml"
                tree = ET.parse(ruta)
                root = tree.getroot()
                base_existente = None
                campo_existente = None


                if os.path.exists(ruta):
                    pass
                else:   #SI NO EXISTE LA BASE DE DATOS
                    ast.escribir_en_consola("ERROR: No existe la base de datos : "+str(nombre_base)+"\n")
                    ast.insertar_error_semantico(ERROR_LSS("SEMANTICO","CONTAR: No existe la base de datos",self.linea))
                    salida = VALOR("ERROR",TIPO.ERROR,self.linea,self.columna)
                    self.tipo = salida.tipo
                    return "ERROR"

                for base in root.findall('base'):
                    if base.attrib['name'] == nombre_base:
                        for tabla in base:
                            if tabla.attrib['name'] == valor_tabla_ref:
                                #VALIDAR EXISTE EL CAMPO
                                numero_campo = ""
                                for campos in tabla.findall('campo'):
                                    for campo in campos.findall('nombre'):
                                        self.numero_campo = self.numero_campo+1
                                        #print(self.numero_campo)
                                        #print(campo.text)
                                        if(campo.text == valor_campo_ref):
                                            campo_existente = campo
                                            break
                                    if(campo_existente is not None):
                                        break
                                        
                                if(campo_existente is not None):

                                    #RECORRER LOS VALORES
                                    #print(self.numero_campo)
                                    for valores in tabla.findall('dato'):
                                        valor1 = valores[self.numero_campo].text
                                        if(valor1 is not None):
                                            res = self.operar(valor1,valor2,self.operacion)
                                            if res == True:
                                                self.cuenta = self.cuenta+1
                                else:
                                    ast.escribir_en_consola("ERROR: El campo "+str(valor_campo_ref)+" no existe en la tabla\n")
                                    ast.insertar_error_semantico(ERROR_LSS("SEMANTICO","CONTAR: El campo"+str(valor_campo_ref)+" no existe en la tabla",self.linea))
                                    salida = VALOR("ERROR",TIPO.ERROR,self.linea,self.columna)
                                    self.tipo = salida.tipo
                                    return "ERROR"

                                base_existente = tabla
                                break
                        if base_existente is not None:
                            break
        if(base_existente is None):
            ast.escribir_en_consola("ERROR: La TABLA "+str(valor_tabla_ref)+" No existe en la base !\n")
            ast.insertar_error_semantico(ERROR_LSS("SEMANTICO","CONTAR: La tabla "+str(valor_tabla_ref+" No existe en la base"),self.linea))
            salida = VALOR("ERROR",TIPO.ERROR,self.linea,self.columna)
            self.tipo = salida.tipo
            return "ERROR"

        respuesta = self.cuenta
        #GENERAMOS OBJETO RESPUESTA CON DATOS QUE PIDE EL ENUNCIADO
        salida = VALOR(respuesta,TIPO.INT,self.linea,self.columna)
        
        #BORRAR
        ast.escribir_en_consola("CONTAR:"+str(self.cuenta)+" \n")
        self.tipo = salida.tipo
        return respuesta
    
