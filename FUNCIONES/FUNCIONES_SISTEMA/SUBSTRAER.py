from FUNCIONES.ARBOL.EJECUCION import *
from FUNCIONES.ARBOL.VALOR import *
from FUNCIONES.ERROR_LSS import *

import xml.etree.ElementTree as ET

class SUBSTRAER(Expresion):        
    def __init__(self, cadena1,inicio, final, linea, columna):
        super().__init__(linea, columna, "SUBSTRAER")
        self.cadena1 = cadena1      #SON OBJETOS VALOR (CADENA)
        self.inicio = inicio        #SON OBJETOS VALOR (INT)
        self.final = final          #SON OBJETOS VALOR (INT)

    def obtener_valor(self, actual, globa, ast):
        #print(self.text)
        if(isinstance(self.inicio,Expresion) and isinstance(self.final,Expresion) and isinstance(self.cadena1,Expresion)):
            num1 = self.inicio.obtener_valor(actual,globa,ast) - 1  #-1 porque en python el inicio es 0 y en el proyecto es 1
            num2 = self.final.obtener_valor(actual,globa,ast)
            cadena = self.cadena1.obtener_valor(actual,globa,ast)

            #tipo_inicio = self.inicio.tipo.obtener_tipo_dato()
            tipo_inicio = self.inicio.tipo.obtener_tipo_dato()
            tipo_final = self.final.tipo.obtener_tipo_dato()
            tipo_cadena = self.cadena1.tipo.obtener_tipo_dato()

            #SI INICIO Y FINAL SON ENTEROS O BIT(1 TAMBIEN ES ENTERO), Y CADENA ES NCHAR O NVARCHAR
            if((tipo_inicio == TIPO.INT or tipo_inicio == TIPO.BIT)and (tipo_final== TIPO.INT or tipo_final == TIPO.BIT)and (tipo_cadena == TIPO.NCHAR or tipo_cadena == TIPO.NVARCHAR) ):
                #EXTRA SI EL INICIO EN MENOR A 0 SE PONE POSICION 0
                
                if(num1<0):
                    num1 = 0
            
                val_respuesta = ""
                #VALIDACION SI EL NUMERO FINAL EXCEDE LA CANTIDAD DE CARACTERES 
                if(num2 > len(cadena)):
                    ast.escribir_en_consola("("+str(self.linea)+")"+"ERROR: El numero final, excede la cantidad de caracteres de la cadena!\n")
                    ast.insertar_error_semantico(ERROR_LSS("SEMANTICO","SUBSTRAER: El numero final excede la cantidad de caracteres de la cadena",self.linea))
                    respuesta = VALOR("ERROR",TIPO.ERROR,self.linea,self.columna)
                    self.tipo = respuesta.tipo
                    return "ERROR"
                for i in range (num1, num2):
                    val_respuesta += cadena[i]
                
                respuesta = VALOR(val_respuesta,TIPO.NVARCHAR,self.linea,self.columna)
                #ast.escribir_en_consola("("+str(self.linea)+")"+"LA NUEVA CADENA ES: "+respuesta.valor +"\n")
                self.tipo = respuesta.tipo
                return val_respuesta
            

            elif(((tipo_cadena == TIPO.COLUMNA) or (tipo_cadena == TIPO.ALIAS)) and (tipo_inicio == TIPO.INT or tipo_inicio == TIPO.BIT) and (tipo_final == TIPO.INT or tipo_final == TIPO.BIT) ):
                nombre_base = ast.obtener_base_activa()
                nombre_tabla = ast.obtener_tabla_activa()
                print(nombre_base)
                print(nombre_tabla)
                ruta = "BASE_DATOS/"+str(nombre_base)+".xml"

                print("SERA COLUMNA O ALIAS")
                if(tipo_cadena == TIPO.COLUMNA):
                    pass
                elif(tipo_cadena == TIPO.ALIAS):
                    pass
                
                obj_tabla = self.obtener_objeto_tabla(ruta,nombre_tabla)
                valor_exp1 = None
                if(tipo_cadena == TIPO.COLUMNA and nombre_tabla != None):
                    valor_exp1 = self.obtener_lista_datos(obj_tabla,cadena)
                elif(tipo_cadena == TIPO.ALIAS):
                    valor_exp1 = cadena
                else:
                    valor_exp1 = cadena
                
                lista_respuesta1 = []
                lista_respuesta1.append(valor_exp1[0])
                lista_respuesta1.append("SUBSTRAER")

                lst_vals = []
                for i in range(len(valor_exp1[2])):
                    val = valor_exp1[2][i]
                    nueva_cadena = ""
                    for j in range(int(num1), int(num2)):
                        try:
                            nueva_cadena+= val[j]
                        except:
                            nueva_cadena+=""

                    lst_vals.append(str(nueva_cadena))
                lista_respuesta1.append(lst_vals)

                val = VALOR("",TIPO.LISTA_COLUMNAS,self.linea,self.columna)
                self.tipo = val.tipo
                return lista_respuesta1
                

            else:
                ast.escribir_en_consola("("+str(self.linea)+")"+"ERROR: Expresiones de tipo incorrecto!\n")
                ast.insertar_error_semantico(ERROR_LSS("SEMANTICO","SUBSTRAER: Expresiones de tipo incorrecto",self.linea))

            
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