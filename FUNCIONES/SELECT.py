from FUNCIONES.ARBOL.EJECUCION import *
from FUNCIONES.ARBOL.VALOR import *
from FUNCIONES.CREAR_BASE import *
from FUNCIONES.ERROR_LSS import *
from FUNCIONES.ARBOL.AST import *

class SELECT(Instruccion):        
    def __init__(self,expresion_select,continuacion_from, linea, columna):
        super().__init__(linea, columna, "CREATE ")
        self.expresion_select =expresion_select 
        self.continuacion_from = continuacion_from

    def ejecutar(self, actual, globa, ast):
        #print(self.text)
        salida = ""
        if(isinstance(ast, AST)):
            base_activa = ast.obtener_base_activa()
            '''if(base_activa == ""):  #SI NO EXISTE LA BASE
                ast.escribir_en_consola("ERROR: No hay una base de datos seleccionada!\n")
                ast.insertar_error_semantico(ERROR_LSS("SEMANTICO","CREATE: No hay una base de datos seleccionada",self.linea))
                return'''
            #print(self.expresion_select)
            #print(len(self.expresion_select))
            if(len(self.expresion_select) == 1 and self.continuacion_from == None): #NO TIENE FROM NI WHERE   VIENE 1 EXPRESION
                ast.tabla_actual = None #PARA QUE DE ERROR EN CUALQUIER EXPRESION QUE USE NOMBRE DE COLUMNA
                expr = self.expresion_select[0]
                if(isinstance(expr,Expresion)):
                    valor_expresion_select = expr.obtener_valor(actual,globa,ast)
                    tipo_expresion_select = expr.tipo.obtener_tipo_dato()
                    if(tipo_expresion_select == TIPO.ASTERISCO):
                        ast.escribir_en_consola("ERROR: Hay * sin FROM!"+ "\n") 
                        return
                        
                    salida += str(valor_expresion_select) + "\n"
 
                    #ast.escribir_en_consola(str(valor_expresion_select) + "\n")    

            elif(len(self.expresion_select) > 1 and self.continuacion_from == None): #NO TIENE FROM NI WHERE  VIENE MAS DE 1 EXPRESION
                ast.tabla_actual = None
                for i in range(len(self.expresion_select)):
                    expr = self.expresion_select[i]
                    if(isinstance(expr, Expresion)):
                        valor_expresion_select = expr.obtener_valor(actual,globa,ast)
                        tipo_expresion_select = expr.tipo.obtener_tipo_dato()
                        #print(tipo_expresion_select)
                        if(tipo_expresion_select == TIPO.COLUMNA):                  #HAY NOMBRES DE COLUMNAS SIN FROM (NO SE PUEDE TRABAJAR)
                            ast.escribir_en_consola("ERROR: Hay nombres de columnas sin FROM!"+ "\n") 
                            return
                        else:
                            #ast.escribir_en_consola(str(valor_expresion_select)+ "\n") 
                            salida+=str(valor_expresion_select)+ "\n"
            elif(len(self.expresion_select) == 1 and self.continuacion_from != None):
                #print("CON FROM")
                expr = self.expresion_select[0]
                valor_expresion_select = expr.obtener_valor(actual,globa,ast)
                tipo_expresion_select = expr.tipo.obtener_tipo_dato()
                valor_from = self.continuacion_from[0]
                valor_where = self.continuacion_from[1]

                if(len(valor_from)== 1 and valor_where == None):    #SI VIENE FROM SIN WHERE
                    tabla_from = valor_from[0].obtener_valor(actual,globa,ast)
                    if(tipo_expresion_select ==TIPO.COLUMNA): #MOSTRAR 1 TABLA EN SALIDA
                        ruta = "BASE_DATOS/"+str(base_activa)+".xml"
                        obj_tabla = self.obtener_objeto_tabla(ruta,tabla_from)
                        if(obj_tabla != None):
                            num_campo = self.encontrar_campo(obj_tabla,valor_expresion_select)
                            salida += "\n\t"
                            salida += str(valor_expresion_select)+"\n"
                            salida += "\t--------------------------\n"
                            for datos in obj_tabla.findall('dato'):
                                if(num_campo != None): 
                                    salida += "\t"+str(datos[num_campo].text)+"\n"
                                else:
                                    salida += "\tPEND\n"
                            
                        
            
            elif(len(self.expresion_select) > 1 and self.continuacion_from != None):
                valor_from = self.continuacion_from[0]
                valor_where = self.continuacion_from[1]
                lista_expresiones = self.expresion_select
                if(len(valor_from)== 1 and valor_where == None):    #SI VIENE FROM SIN WHERE
                    tabla_from = valor_from[0].obtener_valor(actual,globa,ast)
                    ruta = "BASE_DATOS/"+str(base_activa)+".xml"
                    obj_tabla = self.obtener_objeto_tabla(ruta,tabla_from)
                    if(obj_tabla != None):
                        solo_columnas = True
                        lst_orden =[]
                        for expr in lista_expresiones: 
                            valor_expr = expr.obtener_valor(actual,globa,ast)
                            tipo_expr = expr.tipo.obtener_tipo_dato()
                            if(tipo_expr == TIPO.COLUMNA):
                                num = self.encontrar_campo(obj_tabla,valor_expr)
                                salida += "\t"+valor_expr
                                lst_orden.append(num)
                            else: #SI NO ES COLUMNA ES UNA EXPRESION
                                lst_orden.append(expr)
                                solo_columnas = False
                        if(solo_columnas == True):      #HAY MAS DE 1 COLUMNA PERO TODOS SON NOMBRE DE COLUMNAS
                            for dato in obj_tabla.findall('dato'):
                                salida +="\n"
                                for num in lst_orden:
                                    salida +="\t" + str(dato[num].text)
                        else: 
                            lst_numero_orden =[]
                            for dato in obj_tabla.findall('dato'):
                                salida +="\n"
                                for num in lst_orden:
                                    if(isinstance(num,int)):
                                        salida +="\t" + str(dato[num].text)
                                    else:
                                        salida +="\t" + str("PEND")




        ast.escribir_en_consola(str(salida)+"\n")

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