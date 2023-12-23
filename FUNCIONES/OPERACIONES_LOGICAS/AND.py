from FUNCIONES.ARBOL.EJECUCION import *
from FUNCIONES.ARBOL.VALOR import *

class EXP_AND(Expresion):        
    def __init__(self, expr1,expr2, linea, columna):
        super().__init__(linea, columna, "AND")
        self.expr1 = expr1      #SON OBJETOS VALOR
        self.expr2 = expr2

    def obtener_valor(self, actual, globa, ast):
        #print(self.text)
        if(isinstance(self.expr1,Expresion) and isinstance(self.expr2,Expresion)):
            expr1 = self.expr1.obtener_valor(actual,globa,ast)
            expr2 = self.expr2.obtener_valor(actual,globa,ast)
            tipo_expr1 = self.expr1.tipo.obtener_tipo_dato()
            tipo_expr2 = self.expr2.tipo.obtener_tipo_dato()

            #print(tipo_expr1)
            #print(tipo_expr2)
            '''print("\n\nAND")
            print("EXPR1")
            print(expr1)
            print("\nEXPR2")
            print(expr2)'''

            if(tipo_expr1 == TIPO.LISTA_COLUMNAS or tipo_expr2 == TIPO.LISTA_COLUMNAS):
                #EN AND SOLO VAMOS A OBTENER LOS QUE SE REPITEN Y UNIRLOS, SOLO SI SON DE LA MISMA TABLA
                if(tipo_expr1 == TIPO.ERROR or tipo_expr2 == TIPO.ERROR):
                    val = VALOR("",TIPO.ERROR,self.linea,self.columna)
                    self.tipo = val.tipo
                    return None
                lst = []
                for i in range(len(expr1)):
                    lst1 = expr1[i]
                    nombre_t = expr1[i][0]
                    datos_t = expr1[i][2]
                    if(len(lst)!=0):
                        for j in range(len(lst)):
                            nombre_ref = lst[j][0]
                            datos_ref = lst[j][2]
                            if(nombre_ref == nombre_t):
                                #print("LA LISTA YA ESTA EN LA RESPUESTA: COMPARARLO")
                                lst_datos =[]
                                if(len(datos_t) > len(datos_ref)):
                                    for dato_t in datos_t:
                                        if(dato_t in datos_ref):
                                            lst_datos.append(dato_t)                                        
                                else:
                                    for dato_ref in datos_ref:
                                        if(dato_ref in datos_t):
                                            lst_datos.append(dato_ref)
                                lst[j][2] = lst_datos
                                break
                    else:
                        lst.append(lst1)

                for i in range(len(expr2)):
                    lst1 = expr2[i]
                    nombre_t = expr2[i][0]
                    datos_t = expr2[i][2]
                    if(len(lst)!=0):
                        encontro = False
                        for j in range(len(lst)):
                            nombre_ref = lst[j][0]
                            datos_ref = lst[j][2]
                            if(nombre_ref == nombre_t):
                                encontro = True
                                #print("LA LISTA YA ESTA EN LA RESPUESTA: COMPARARLO")
                                lst_datos =[]
                                if(len(datos_t) > len(datos_ref)):
                                    for dato_t in datos_t:
                                        if(dato_t in datos_ref):
                                            lst_datos.append(dato_t)
                                else:
                                    for dato_ref in datos_ref:
                                        if(dato_ref in datos_t):
                                            lst_datos.append(dato_ref)
                                lst[j][2] = lst_datos
                                break
                        if(encontro == False):
                            lst.append(lst1)
                    else:
                        lst.append(lst1)

                val = VALOR("",TIPO.LISTA_COLUMNAS,self.linea,self.columna)
                self.tipo = val.tipo
                return lst
                

            if(((tipo_expr1==TIPO.INT or tipo_expr1==TIPO.BIT or tipo_expr1==TIPO.DECIMAL)and(tipo_expr2==TIPO.INT or tipo_expr2==TIPO.BIT or tipo_expr2==TIPO.DECIMAL))):
                if((int(expr1)==0 or int(expr1)==1) and(int(expr2)==0 or int(expr2)==1)):
                    if((expr1 == 1) and expr2 == 1):
                        respuesta = VALOR(1,TIPO.BIT,self.linea,self.columna)   #1= VERDADERO
                    else:
                        respuesta = VALOR(0,TIPO.BIT,self.linea,self.columna)   #1= VERDADERO
                else:
                    respuesta = VALOR("ERROR",TIPO.ERROR,self.linea,self.columna)   #0= FALSO

            #EXTRA PORQUE NO SE ENTRA TAMBIEN
            elif((tipo_expr1 == TIPO.NCHAR or tipo_expr1 == TIPO.NVARCHAR)and (tipo_expr2 == TIPO.NCHAR or tipo_expr2 == TIPO.NVARCHAR)):
                if(expr1.lower() == "verdadero" and expr2.lower() == "verdadero"):
                    respuesta = VALOR(1,TIPO.BIT,self.linea,self.columna)
                elif (expr1.lower() == "verdadero" and expr2.lower() == "falso"):
                    respuesta = VALOR(0,TIPO.BIT,self.linea,self.columna)
                elif (expr1.lower() == "falso" and expr2.lower() == "verdadero"):
                    respuesta = VALOR(0,TIPO.BIT,self.linea,self.columna)
                elif (expr1.lower() == "falso" and expr2.lower() == "falso"):
                    respuesta = VALOR(0,TIPO.BIT,self.linea,self.columna)
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