from FUNCIONES.ARBOL.EJECUCION import *
from FUNCIONES.ARBOL.VALOR import *
from FUNCIONES.CREAR_BASE import *
from FUNCIONES.ERROR_LSS import *
from FUNCIONES.ARBOL.AST import *
from FUNCIONES.EXPRESION_SELECT import *
from FUNCIONES.FUNCIONES_SISTEMA.SELECT_SUMA import *
from FUNCIONES.FUNCIONES_SISTEMA.CONTAR import *

class SELECT(Instruccion):        
    def __init__(self,expresion_select,continuacion_from, linea, columna):
        super().__init__(linea, columna, "CREATE ")
        self.expresion_select =expresion_select 
        self.continuacion_from = continuacion_from

    def ejecutar(self, actual, globa, ast):
        print(self.text)
        salida = ""
        if(isinstance(ast, AST)):
            base_activa = ast.obtener_base_activa()
            #if(base_activa == ""):  #SI NO EXISTE LA BASE
            #    ast.escribir_en_consola("ERROR: No hay una base de datos seleccionada!\n")
            #    ast.insertar_error_semantico(ERROR_LSS("SEMANTICO","CREATE: No hay una base de datos seleccionada",self.linea))
            #    return
            if(len(self.expresion_select) == 1 and self.continuacion_from == None): #1 EXPRESION, NO TIENE FROM, NO TIENE WHERE
                ast.tabla_actual = None #PARA QUE DE ERROR EN CUALQUIER EXPRESION QUE USE NOMBRE DE COLUMNA
                expr = self.expresion_select[0]
                if(isinstance(expr,Expresion)):
                    valor_expresion_select = expr.obtener_valor(actual,globa,ast)
                    tipo_expresion_select = expr.tipo.obtener_tipo_dato()
                    if(tipo_expresion_select == TIPO.ASTERISCO):
                        ast.escribir_en_consola("("+str(self.linea)+")"+"ERROR: Hay * sin FROM!"+ "\n") 
                        ast.insertar_error_semantico(ERROR_LSS("SEMANTICO","SELECT: Hay * sin FROM",self.linea))
                        return 
                    salida += str(valor_expresion_select) + "\n"   

            elif(len(self.expresion_select) > 1 and self.continuacion_from == None): # MAS DE 1 EXPRESION, NO TIENE FROM, NO TIENE WHERE
                ast.tabla_actual = None
                for i in range(len(self.expresion_select)):
                    expr = self.expresion_select[i]
                    if(isinstance(expr, Expresion)):
                        valor_expresion_select = expr.obtener_valor(actual,globa,ast)
                        tipo_expresion_select = expr.tipo.obtener_tipo_dato()
                        if(tipo_expresion_select == TIPO.COLUMNA):                  #HAY NOMBRES DE COLUMNAS SIN FROM (NO SE PUEDE TRABAJAR)
                            ast.escribir_en_consola("("+str(self.linea)+")"+"ERROR: Hay nombres de columnas sin FROM!"+ "\n") 
                            ast.insertar_error_semantico(ERROR_LSS("SEMANTICO","SELECT: Hay nombres de columnas sin FROM",self.linea))
                            return
                        else:
                            salida+=str(valor_expresion_select)+ "\n"
  
            elif(len(self.expresion_select) >= 1 and self.continuacion_from != None):
                valor_from = self.continuacion_from[0]
                valor_where = self.continuacion_from[1]
                lista_expresiones = self.expresion_select
                if(len(valor_from)>= 1 and valor_where == None):                      #MAS DE 1 FROM, NO TIENE WHERE

                    tabla_from = valor_from[0].obtener_valor(actual,globa,ast)
                    
                    valores_froms = []                                                  #CONVERTIR LISTA DE VALORES A LISTA DE STRINGS
                    for val in valor_from:
                        valores_froms.append(val.obtener_valor(actual,globa,ast))
                    ruta = "BASE_DATOS/"+str(base_activa)+".xml"
                    lst_orden =[]
                    solo_columnas = True

                    #VALIDAR SI ES UN ASTERISCO
                    ast.usar_tabla(tabla_from)

                    expr_temp = lista_expresiones[0].obtener_valor(actual,globa,ast)
                    tipo_expr_temp = lista_expresiones[0].tipo.obtener_tipo_dato()
                    #print(tipo_expr)
                    
                    
                    

                    if(tipo_expr_temp == TIPO.ASTERISCO):  #SOLO UN CASO PUEDE TENER ESTO Y ES CUANDO VIENE *
                        
                        print("VIENE *")
                        for tab in valores_froms:
                            obj_tabla = self.obtener_objeto_tabla(ruta,tab)
                            #RECORRE CATA TABLA Y OBTIENE CADA COLUMNA
                            if(obj_tabla != None):
                                for campos in obj_tabla.findall('campo'):
                                    lst_orden.append(self.obtener_lista_datos(obj_tabla,campos[0].text))
                        #print(lst_orden)
                    
                    else:   #SI NO ES UN ASTERISCO TODO NORMAL
                        ast.usar_tabla(tabla_from)
                        obj_tabla = self.obtener_objeto_tabla(ruta,tabla_from)
                        if(obj_tabla != None):
                            
                            #GUARDADO DE DATOS EN LISTAS
                            for expr in lista_expresiones: #OBTIENE LOS VALORES DE LAS EXPRESIONES Y LAS GUARDA EN LISTAS

                                valor_expr = expr.obtener_valor(actual,globa,ast)
                                print(valor_expr)
                                if(isinstance(expr,SELECT_SUMA)):                                   
                                    salida += "SUMA: "+str(valor_expr)
                                    salida += "\n"
                                    continue
                                elif(isinstance(expr, CONTAR)):
                                    salida += "CONTAR: "+str(valor_expr)
                                    salida += "\n"
                                    continue
                                    
                                #print(expr)
                                #print(valor_expr)
                                tipo_expr = expr.tipo.obtener_tipo_dato()


                                if(tipo_expr == TIPO.COLUMNA):                                      #ES COLUMNA
                                    lista_colum = self.obtener_lista_datos(obj_tabla,valor_expr)
                                    if(lista_colum !=None):
                                        lst_orden.append(lista_colum)    
                                    else:
                                        ast.escribir_en_consola("("+str(self.linea)+")"+"ERROR: La columna " +str(valor_expr)+" No existe en la tabla "+str(tabla_from)+"!\n")
                                        return
                                elif(tipo_expr == TIPO.ALIAS):                                      #ES TABLA.COLUMNA
                                    print("ALI")
                                    print(valor_expr)
                                    if(valor_expr!=None):
                                        lst_orden.append(valor_expr)
                                    else:
                                        ast.escribir_en_consola("("+str(self.linea)+")"+"ERROR: NO existe la columna "+str(expr.nombre_columna) +" en la tabla "+str(expr.nombre_tabla)+"!\n")
                                else:           
                                    if(valor_expr!= None):                                                     #ES UNA EXPRESION
                                        lst_orden.append(valor_expr)

                    #RECORRER COLUMNAS PARA MOSTRAR
                    tablas_res = []
                    num_datos_res = []
                    lista_columnas = []
                    
                    for lis in lst_orden:  #OBTIENE EL NUMERO DE TABLAS, DATOS DE LAS RESPUESTAS DEL SELECT
                        print("RES: "+str(lis))
                        nombre_tabla = lis[0]
                        nombre_columna = lis[1]
                        valores = lis[2]
                        if(nombre_tabla in tablas_res):
                            lista_columnas[tablas_res.index(nombre_tabla)].append(nombre_columna)
                        else:
                            tablas_res.append(nombre_tabla)
                            num_datos_res.append(len(valores))
                            lista_columnas.append([nombre_columna])

                    for i in range(len(valores_froms)):    #RECORRE LA LISTA DE NOMBRES DEL FROM
                        tabla_actual = valores_froms[i]
                        salida += "TABLA: "+str(tabla_actual) +"\n"
                        pos_tabla = None


                        #MOSTRADO DE TABLAS EN SALIDA
                        for j in range(len(tablas_res)):    #RECORRE NOMBRES DE TABLAS DE LA RESPUESTA PARA BUSCAR SI SE REALIZO BUSQUEDA U OPERACION
                            tb = tablas_res[j]
                            if(tb == tabla_actual):
                                pos_tabla = j
                                break
                    
                        if(pos_tabla != None):
                            #MOSTRAR COLUMNAS
                            salida += "------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n"
                            for columna in lista_columnas[pos_tabla]:
                                salida += "\t"+str(columna)
                            salida+="\n"
                            salida += "------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n"
                            for j in range (num_datos_res[pos_tabla]):    #RECORRE EL NUMERO DE DATOS DE LA TABLA
                                for k in range(len(lst_orden)):           #RECORRE CADA LISTA DE DATOS BUSCANDO VALORES DE LA TABLA
                                    lista_resp = lst_orden[k]
                                    if(lista_resp[0] == tabla_actual):   #SI ENCUENTRA LA TABLA
                                        valores = lista_resp[2]          
                                        salida += "\t" +str(valores[j]) #AGREGA EL VALOR A LA SALIDA
                                        continue
                                salida += "\n"
                            salida += "\n\n\n"
                
                if(valor_where != None):
                    if(len(valor_from) >= 1 and len(valor_where) >= 1):
                        tabla_from = valor_from[0].obtener_valor(actual,globa,ast)
                        ast.usar_tabla(tabla_from)
                        lista_where = valor_where[0]
                        #print("OBTENIENDO WHERES")
                        validaciones = lista_where.obtener_valor(actual,globa,ast)      #OBTENCION DE LISTA DE VALIDACIONES DEL WHERE
                        #print("FIN WHERES")
                        if(validaciones == None):       #SI WHERE ES NONE ES PORQUE HUBO UN ERROR
                            ast.escribir_en_consola("("+str(self.linea)+")"+"ERROR: Se encontro un error en el where!\n")
                            return 
                        
                        valores_froms = []                                                  #CONVERTIR LISTA DE VALORES A LISTA DE STRINGS
                        for val in valor_from:
                            valores_froms.append(val.obtener_valor(actual,globa,ast))
                        ruta = "BASE_DATOS/"+str(base_activa)+".xml"
                        lst_orden =[]
                        print("EMPEZANDO SELECT")
                        #VALIDAR SI ES UN ASTERISCO
                        expr = lista_expresiones[0].obtener_valor(actual,globa,ast)
                        tipo_expr = lista_expresiones[0].tipo.obtener_tipo_dato()
                    
                        if(tipo_expr == TIPO.ASTERISCO):  #SOLO UN CASO PUEDE TENER ESTO Y ES CUANDO VIENE *
                            for tab in valores_froms:
                                obj_tabla = self.obtener_objeto_tabla(ruta,tab)
                                #RECORRE CATA TABLA Y OBTIENE CADA COLUMNA
                                if(obj_tabla != None):
                                    for campos in obj_tabla.findall('campo'):
                                        lst_orden.append(self.obtener_lista_datos(obj_tabla,campos[0].text))
                        
                        else:   #SI NO ES UN ASTERISCO TODO NORMAL
                            ast.usar_tabla(tabla_from)
                            obj_tabla = self.obtener_objeto_tabla(ruta,tabla_from)
                            if(obj_tabla != None):
                                
                                #GUARDADO DE DATOS EN LISTAS
                                for expr in lista_expresiones: #OBTIENE LOS VALORES DE LAS EXPRESIONES Y LAS GUARDA EN LISTAS
                                    if(isinstance(expr,SELECT_SUMA)): 
                                        expr.validaciones_where = validaciones    
                                        val = expr.obtener_valor(actual,globa,ast)                            
                                        salida += "SUMA: "+str(val)
                                        salida += "\n"
                                        continue
                                    elif(isinstance(expr, CONTAR)):
                                        expr.validaciones_where = validaciones  
                                        val = expr.obtener_valor(actual,globa,ast) 
                                        salida += "CONTAR: "+str(val)
                                        salida += "\n"
                                        continue
                                    valor_expr = expr.obtener_valor(actual,globa,ast)
                                    tipo_expr = expr.tipo.obtener_tipo_dato()

                                    



                                    if(tipo_expr == TIPO.COLUMNA):                                      #ES COLUMNA
                                        lista_colum = self.obtener_lista_datos(obj_tabla,valor_expr)
                                        if(lista_colum !=None):
                                            lst_orden.append(lista_colum)    
                                        else:
                                            ast.escribir_en_consola("("+str(self.linea)+")"+"ERROR: La columna " +str(valor_expr)+" No existe en la tabla "+str(tabla_from)+"!\n")
                                            ast.insertar_error_semantico(ERROR_LSS("SEMANTICO","SELECT: La columna " +str(valor_expr)+" No existe en la tabla",self.linea))
                                            return
                                    elif(tipo_expr == TIPO.ALIAS):                                      #ES TABLA.COLUMNA
                                        if(valor_expr!=None):
                                            lst_orden.append(valor_expr)
                                        else:
                                            ast.escribir_en_consola("("+str(self.linea)+")"+"ERROR: NO existe la columna "+str(expr.nombre_columna) +" en la tabla "+str(expr.nombre_tabla)+"!\n")
                                            ast.insertar_error_semantico(ERROR_LSS("SEMANTICO","SELECT:NO existe la columna "+str(expr.nombre_columna) +" en la tabla "+str(expr.nombre_tabla),self.linea))
                                    elif(tipo_expr == TIPO.EXPRESION_SELECT):
                                        print("VAMOS A VER SI ES UN OBJETO EXPRESION SELECT")
                                        if(isinstance(valor_expr, EXPRESION_SELECT)):
                                            print("SI ES EXPRESION SELECT")
                                            lst_orden.append(valor_expr)
                                           

                                    else:           
                                        if(valor_expr!= None):                                          #ES UNA EXPRESION
                                            lst_orden.append(valor_expr)

                        #RECORRER COLUMNAS PARA MOSTRAR
                        tablas_res = []
                        num_datos_res = []
                        lista_columnas = []
                        for lis in lst_orden:  #OBTIENE EL NUMERO DE TABLAS, DATOS DE LAS RESPUESTAS DEL SELECT
                            nombre_tabla = lis[0]
                            nombre_columna = lis[1]
                            valores = lis[2]
                            if(nombre_tabla in tablas_res):
                                lista_columnas[tablas_res.index(nombre_tabla)].append(nombre_columna)
                            else:
                                tablas_res.append(nombre_tabla)
                                num_datos_res.append(len(valores))
                                lista_columnas.append([nombre_columna])

                        for i in range(len(valores_froms)):    #RECORRE LA LISTA DE NOMBRES DEL FROM
                            tabla_actual = valores_froms[i]
                            salida += "TABLA: "+str(tabla_actual) +"\n"
                            pos_tabla = None

                            #MOSTRADO DE TABLAS EN SALIDA
                            for j in range(len(tablas_res)):    #VALIDA QUE EN LAS RESPUESTAS DEL SELECT ESTE EL NOMBRE DE LA TABLA
                                tb = tablas_res[j]
                                if(tb == tabla_actual):
                                    pos_tabla = j
                                    break
                        
                            if(pos_tabla != None):
                                #MOSTRAR COLUMNAS
                                salida += "------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n"
                                for columna in lista_columnas[pos_tabla]:
                                    salida += "\t"+str(columna)
                                salida+="\n"
                                salida += "------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n"
                                
                                mostro = False
                                for j in range (num_datos_res[pos_tabla]):    #RECORRE EL NUMERO DE DATOS DE LA TABLA
                                    for k in range(len(lst_orden)):           #RECORRE CADA LISTA DE DATOS BUSCANDO VALORES DE LA TABLA
                                        esta_val = False
                                        lista_resp = lst_orden[k]
                                        valores = lista_resp[2]   
                                        if(lista_resp[0] == tabla_actual):   #SI ENCUENTRA LA TABLA

                                            #VALIDAR QUE EXISTA ESTA POSICION EN LA TABLA DE WHERE PARA MOSTRARLA
                                            for vals in validaciones:
                                                nom_tabla = vals[0]
                                                if(nom_tabla == tabla_actual):
                                                    esta_val = True
                                                    datos_ref = vals[2]
                                                    if(j in datos_ref):
                                                        salida += "\t" +str(valores[j]) #AGREGA EL VALOR A LA SALIDA
                                                        mostro =True
                                                        break
                                            if(esta_val == False):
                                                salida += "\t" +str(valores[j])
                                                mostro = True
                                                #MOSTRARLO NORMAL
                                            continue
                                    if(mostro == True):
                                        salida += "\n"
                                salida += "\n\n\n"
        ast.escribir_en_consola(str(salida)+"\n")

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
            print(campos[0].text)
            print(nomcampo)
            if(campos[0].text == nomcampo):
                print("ENCONTRADOS")
                val = True
                break
        if(val == True):
            for dato in objeto_tabla.findall('dato'):
                lst_res.append(dato[contador].text)
        else:
            return None
        lst_prin.append(lst_res)
        return lst_prin             #[nombre_tabla, nombre_campo ,[valor,valor]]
                
    def encontrar_campo(self, objeto_tabla, nomcampo):
        contador = -1
        for campos in objeto_tabla.findall('campo'):
            contador +=1
            if(campos[0].text == nomcampo):
                return contador
        return None