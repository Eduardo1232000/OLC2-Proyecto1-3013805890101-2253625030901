from FUNCIONES.ARBOL.EJECUCION import *
from FUNCIONES.ARBOL.VALOR import *
import xml.etree.ElementTree as ET

class DIFERENTE(Expresion):        
    def __init__(self, expr1,expr2, linea, columna):
        super().__init__(linea, columna, "DIFERENTE")
        self.expr1 = expr1      #SON OBJETOS VALOR
        self.expr2 = expr2

    def obtener_valor(self, actual, globa, ast):
        #print(self.text)
        if(isinstance(self.expr1,Expresion) and isinstance(self.expr2,Expresion)):
            expr1 = self.expr1.obtener_valor(actual,globa,ast)
            expr2 = self.expr2.obtener_valor(actual,globa,ast)
            tipo_expr1 = self.expr1.tipo.obtener_tipo_dato()
            tipo_expr2 = self.expr2.tipo.obtener_tipo_dato()
            if(tipo_expr1 == TIPO.COLUMNA or tipo_expr2 == TIPO.COLUMNA):
                if(tipo_expr1 == TIPO.ERROR or tipo_expr2 == TIPO.ERROR):
                    val = VALOR("",TIPO.ERROR,self.linea,self.columna)
                    self.tipo = val.tipo
                    return None
                #print("SERA COLUMNA")
                #VALIDACION DE COLUMNAS
                nombre_base = ast.obtener_base_activa()
                nombre_tabla = ast.obtener_tabla_activa()
                #print(nombre_tabla)
                ruta = "BASE_DATOS/"+str(nombre_base)+".xml"
                obj_tabla = self.obtener_objeto_tabla(ruta,nombre_tabla)
                valor_exp1 = None
                valor_exp2 = None
                if(tipo_expr1 == TIPO.COLUMNA and nombre_tabla != None):
                    valor_exp1 = self.obtener_lista_datos(obj_tabla,expr1)
                elif(tipo_expr1 == TIPO.ALIAS):
                    valor_exp1 = expr1
                else:
                    valor_exp1 = expr1
                if(tipo_expr2 == TIPO.COLUMNA and nombre_tabla != None):
                    valor_exp2 = self.obtener_lista_datos(obj_tabla,expr2)
                elif(tipo_expr2 == TIPO.ALIAS):
                    valor_exp2 = expr1
                else:
                    valor_exp2 = expr2

                if((tipo_expr1 == TIPO.COLUMNA or tipo_expr1 == TIPO.ALIAS)  and (tipo_expr2 == TIPO.COLUMNA or tipo_expr2 == TIPO.ALIAS)):
                    lista_respuesta1 = []
                    lista_respuesta1.append(valor_exp1[0])
                    lista_respuesta1.append(valor_exp1[1])
                    datos_1 = []
                    lista_respuesta2 = []
                    lista_respuesta1.append(valor_exp2[0])
                    lista_respuesta1.append(valor_exp2[1])
                    datos_2 = []

                    for i in range(len(valor_exp1[2])):
                        val = valor_exp1[2][i]
                        for j in range(len(valor_exp2[2])):
                            val2 = valor_exp2[2][j]
                            if(str(val) != str(val2)):
                                if(i in datos_1):
                                    pass
                                else:
                                    datos_1.append(i)
                                if(j in datos_2):
                                    pass
                                else:
                                    datos_2.append(j)
                    lista_respuesta1.append(datos_1)
                    lista_respuesta2.append(datos_2)


                    res = []
                    res.append(lista_respuesta1)
                    res.append(lista_respuesta2)
                    val = VALOR("",TIPO.LISTA_COLUMNAS,self.linea,self.columna)
                    self.tipo = val.tipo
                    #print(res)
                    return res
                elif(tipo_expr1 == TIPO.COLUMNA or tipo_expr1 == TIPO.ALIAS):
                    lista_respuesta1 = []
                    lista_respuesta1.append(valor_exp1[0])
                    lista_respuesta1.append(valor_exp1[1])
                    datos_1 = []
                    for i in range(len(valor_exp1[2])):
                        val = valor_exp1[2][i]
                        if(str(val) != str(valor_exp2)):
                            if(i in datos_1):
                                pass
                            else:
                                datos_1.append(i)
                    lista_respuesta1.append(datos_1)
                    res = []
                    res.append(lista_respuesta1)
                    val = VALOR("",TIPO.LISTA_COLUMNAS,self.linea,self.columna)
                    self.tipo = val.tipo
                    #print(res)
                    return res
                
                elif(tipo_expr2 == TIPO.COLUMNA or tipo_expr2 == TIPO.ALIAS):
                    lista_respuesta1 = []
                    lista_respuesta1.append(valor_exp2[0])
                    lista_respuesta1.append(valor_exp2[1])
                    datos_1 = []
                    for i in range(len(valor_exp2[2])):
                        val = valor_exp2[2][i]
                        if( valor_exp1 != val):
                            if(i in datos_1):
                                pass
                            else:
                                datos_1.append(i)
                    lista_respuesta1.append(datos_1)
                    res = []
                    res.append(lista_respuesta2)
                    val = VALOR("",TIPO.LISTA_COLUMNAS,self.linea,self.columna)
                    self.tipo = val.tipo
                    #print(res)
                    return res
                else:
                    print("ERROR INESPERADO EN IGUAL")

            if((tipo_expr1 == tipo_expr2) or ((tipo_expr1==TIPO.INT or tipo_expr1==TIPO.BIT or tipo_expr1==TIPO.DECIMAL)and(tipo_expr2==TIPO.INT or tipo_expr2==TIPO.BIT or tipo_expr2==TIPO.DECIMAL))):
                if(expr1 != expr2):
                    respuesta = VALOR(1,TIPO.BIT,self.linea,self.columna)   #1= VERDADERO
                else:
                    respuesta = VALOR(0,TIPO.BIT,self.linea,self.columna)   #0= FALSO
            else:
                respuesta = VALOR(1,TIPO.BIT,self.linea,self.columna)   #0= FALSO
        else:
            respuesta = VALOR("ERROR",TIPO.ERROR,self.linea,self.columna)
        #BORRAR
        #ast.escribir_en_consola("LA RESPUESTA ES: "+str(respuesta.valor) +"\n")
        self.tipo = respuesta.tipo
        return respuesta.obtener_valor(actual,globa,ast)
    

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