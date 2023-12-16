from FUNCIONES.ARBOL.EJECUCION import *
from FUNCIONES.ARBOL.VALOR import *
from FUNCIONES.CREAR_BASE import *
from FUNCIONES.ARBOL.TABLA_FUNCIONES_VARIABLES import *
from FUNCIONES.ARBOL.AST import *
from FUNCIONES.ERROR_LSS import *
from FUNCIONES.SSL.RETURN import *

import gramatica

from FUNCIONES.ARBOL.TABLA_FUNCIONES_VARIABLES import *

class CREATE_FUNCION_BASE(Instruccion):        
    def __init__(self,nombre,retorno,tipo_v,lista_variables,lista_instruccion, linea, columna):
        super().__init__(linea, columna, "CREATE FUNCION ")
   #SON OBJETOS VALOR
        self.nombre = nombre    #VALOR
        self.tipo = tipo_v      #STRING
        self.retorno = retorno
        self.lista_variables = lista_variables #LISTA NOMBRES DE VARIABLES A GUARDAR
        self.lista_instruccion = lista_instruccion #LISTA DE OBJETOS INSTRUCCION O EXPRESION

    def ejecutar(self, actual, globa, ast):
        if(isinstance(actual,TABLA_FUNCIONES_Y_VARIABLES) and isinstance(globa,TABLA_FUNCIONES_Y_VARIABLES) and isinstance(ast, AST) and isinstance(self.nombre, Expresion) and isinstance(self.retorno,TIPODATO)):
            nombre_base = ast.obtener_base_activa()
            nombre_func = self.nombre.obtener_valor(actual,globa,ast)
            tipo_retorno = self.retorno.obtener_tipo_dato()
            size_tipo_retorno = self.retorno.obtener_size()
            lista_parametros = []
            for var in self.lista_variables:
                if(isinstance(var[0], Expresion) and isinstance(var[1],TIPODATO)):
                    nombre_variable = var[0].obtener_valor(actual,globa,ast)
                    if(var[1].tipo == TIPO.INT):
                        tipo_var = "INT"
                        size_tipo_var = 0
                    elif(var[1].tipo == TIPO.DECIMAL):
                        tipo_var = "DECIMAL"
                        size_tipo_var = 0
                    elif(var[1].tipo == TIPO.DATE):
                        tipo_var = "DATE"
                        size_tipo_var = 0
                    elif(var[1].tipo == TIPO.DATETIME):
                        tipo_var = "DATETIME"
                        size_tipo_var = 0
                    elif(var[1].tipo == TIPO.NCHAR):
                        tipo_var = "NCHAR"
                        if(isinstance(var[1],TIPODATO)):
                            size_tipo_var = var[1].obtener_size()
                    elif(var[1].tipo == TIPO.NVARCHAR):
                        tipo_var = "NVARCHAR"
                        if(isinstance(var[1],TIPODATO)):
                            size_tipo_var = var[1].obtener_size()
                    else:
                        tipo_var = "ERROR"
                        ast.escribir_en_consola("ERROR: No se reconocio un tipo de dato\n")
                        ast.insertar_error_semantico(ERROR_LSS("SEMANTICO","CREATE: No se reconocio un tipo de dato",self.linea))
                        return
                    lst = []
                    lst.append(nombre_variable)
                    lst.append(tipo_var)
                    lst.append(size_tipo_var)
                    lista_parametros.append(lst)

            #AGREGAR EL FUNCION A LA BASE
            ruta = "BASE_DATOS/"+str(nombre_base)+".xml"
            tree = ET.parse(ruta)
            root = tree.getroot()
            #VALIDAR QUE NO HAYA UN FUNCION CON MISMO NOMBRE
            for base in root.findall('base'):
                for proc in base.findall('funcion'):
                    if(proc).attrib['name'] == nombre_func:
                        ast.escribir_en_consola("ERROR: Ya existe una funcion con ese nombre\n")
                        ast.insertar_error_semantico(ERROR_LSS("SEMANTICO","CREATE: Ya existe una funcion con ese nombre",self.linea))
                        return 
                    
            for base in root.findall('base'):
                if base.attrib['name'] == nombre_base:
                    nueva_funcion = ET.SubElement(base, 'funcion')
                    nueva_funcion.set('name', nombre_func)  

                    nuevo_retorno = ET.SubElement(nueva_funcion, 'retorno')
                    nuevo_retorno.set('type', str(tipo_retorno))
                    nuevo_retorno.set('size', str(size_tipo_retorno))

                    nuevo_parameters = ET.SubElement(nueva_funcion, 'parameters')
                    for param in lista_parametros:
                        nuevo_param = ET.SubElement(nuevo_parameters, 'parameter')
                        nuevo_param.set('name', str(param[0]))
                        nuevo_param.set('type', str(param[1]))
                        nuevo_param.set('size', str(param[2]))

                    nuevo_sentencias = ET.SubElement(nueva_funcion, 'sentencias')
                    for sent in self.lista_instruccion[0]:
                        nuevo_sent = ET.SubElement(nuevo_sentencias, 'sentencia')
                        nuevo_sent.text = sent.text

                    xml_string = xml.dom.minidom.parseString(ET.tostring(root)).toprettyxml(indent="    ")

                    # Eliminar líneas en blanco
                    lines = xml_string.split('\n')
                    xml_string = '\n'.join(line for line in lines if line.strip())

                    with open(ruta, 'w', encoding='utf-8') as archivo:
                        archivo.write(xml_string)
            ast.escribir_en_consola("FUNCION CREADA\n")

class EJECUTAR_FUNCION_BASE(Expresion):
    def __init__(self,id,lista_valores, linea, columna):
        super().__init__(linea, columna, "EJECUTAR FUNCION")
        self.id = id
        self.lista_valores = lista_valores

    def obtener_valor(self, actual, globa, ast):
        if(isinstance(actual,TABLA_FUNCIONES_Y_VARIABLES) and isinstance(globa,TABLA_FUNCIONES_Y_VARIABLES) and isinstance(ast, AST) and isinstance(self.id,Expresion)):
            nombre_base = ast.obtener_base_activa()
            nombre_funcion = self.id.obtener_valor(actual,globa,ast)
           
            #VALIDAR QUE EXISTA LA FUNCION EN LA BASE
            ruta = "BASE_DATOS/"+str(nombre_base)+".xml"
            tree = ET.parse(ruta)
            root = tree.getroot()

            lista_parametros = []
            lista_sentencias = []
            tipo_retorno = ""
            size_retorno=0
            sentencias_unidas = ""

            #VALIDAR QUE NO HAYA UNA FUNCION CON MISMO NOMBRE
            existe_proc = False
            for base in root.findall('base'):
                for proc in base.findall('funcion'):
                    if(proc).attrib['name'] == nombre_funcion:
                        existe_proc = True
                        for retorn in proc.findall("retorno"):
                            tipo_retorno = retorn.attrib['type']
                            size_retorno = int(retorn.attrib['size'])
                        for params in proc.findall("parameters"):
                            for param in params:
                                objeto_variable = VARIABLE(param.attrib['name'],param.attrib['type'],int(param.attrib['size']),"")
                                lista_parametros.append(objeto_variable)
                        for sentens in proc.findall("sentencias"):
                            for senten in sentens:
                                sentencias_unidas += senten.text 
                                sentencias_unidas += "\n"
            if(existe_proc == False):
                ast.escribir_en_consola("ERROR: No existe la funcion "+str(nombre_funcion)+" En la base "+str(nombre_base)+"\n")
                ast.insertar_error_semantico(ERROR_LSS("SEMANTICO","EXEC: No existe la funcion "+str(nombre_funcion)+" En la base "+str(nombre_base),self.linea))
                return
            
            #ANALIZAR LAS SENTENCIAS CON EL PARSER
            respuesta_parser = gramatica.parses(sentencias_unidas)
            
            if(respuesta_parser !=None):
                respuesta = respuesta_parser[0]
                objeto_funcion = FUNCION(nombre_funcion,tipo_retorno,size_retorno,lista_parametros,respuesta)
                #print(lista_parametros)
                #AGREGARLO EN LA TABLA DE SIMBOLOS
                ast.guardar_en_tabla_simbolos(nombre_funcion,"FUNCION","-",nombre_base, objeto_funcion.obtener_tipo(),actual.nombre,"-",self.linea,self.columna)
                #SE AGREGA SI NO EXISTE (GANAS DE HACERLO, NO SE VA A OBTENER NUNCA)
                validacion_existe = actual.funcion_existe(nombre_funcion)
                if(validacion_existe == False):
                    actual.agregar_funcion_tabla(nombre_funcion,objeto_funcion)
                    
                #RECICLAR EL OTRO EXEC FUNCION
                parametros_funcion = objeto_funcion.obtener_parametros()
                instrucciones_funcion = objeto_funcion.obtener_sentencias()

                #print(parametros_funcion)
                #print(instrucciones_funcion)

                #VALIDACION NUMERO DE VALORES COINCIDE CON NUMERO DE PARAMETROS
                if(len(parametros_funcion) != len(self.lista_valores)):
                    ast.escribir_en_consola("ERROR: El numero de parametros no coincide con el numero de variables del procedimiento\n")
                    ast.insertar_error_semantico(ERROR_LSS("SEMANTICO","EXEC: El numero de parametros no coincide con el numero de variables del procedimiento",self.linea))
                    return
                                
                #CREAR EL AMBITO DE FUNCION
                ambito_funcion = TABLA_FUNCIONES_Y_VARIABLES(actual,nombre_funcion)

                #GUARDA LOS VALORES EN LOS PARAMETROS
                for i in range(len(self.lista_valores)):
                    lista_valor_variable = self.lista_valores[i]
                    objeto_variable_guardar = lista_valor_variable[0]
                    objeto_valor_variable = lista_valor_variable[1]
                    #print(self.lista_valores)
                    #print(lista_valor_variable)
                    #print(objeto_variable_guardar)
                    #print(objeto_valor_variable)
                    if(isinstance(objeto_variable_guardar, Expresion) and isinstance(objeto_valor_variable, Expresion)):   #SI TIENE NOMBRES DE VARIABLES
                        variable_guardar = objeto_variable_guardar.obtener_valor(actual,globa,ast)
                        valor_variable = objeto_valor_variable.obtener_valor(actual,globa,ast)
                        #print(variable_guardar)
                        #print(valor_variable)

                        for j in range (len(parametros_funcion)):
                            var = parametros_funcion[j]
                            if(isinstance(var,VARIABLE)):

                                nombre_var = var.obtener_nombre()
                                if(nombre_var != variable_guardar): #SI NO ES EL MISMO NOMBRE PASA AL SIGUIENTE
                                    continue

                                #print("ENCONTRE")
                                tipo_var = var.obtener_tipo()
                                tipo_valor = objeto_valor_variable.tipo.obtener_tipo_dato()

                                #VALIDACION TIPOS
                                if(tipo_var != tipo_valor):
                                    print(tipo_var)
                                    print(tipo_valor)
                                    if((tipo_var == "NCHAR" or tipo_var == "NVARCHAR")and (tipo_valor == "NCHAR" or tipo_valor == "NVARCHAR")):
                                        pass
                                    else:
                                        ast.escribir_en_consola("ERROR: El valor "+str(valor_variable)+" no es del tipo correcto en la funcion\n")
                                        ast.insertar_error_semantico(ERROR_LSS("SEMANTICO","EXEC: El valor "+str(valor_variable)+" no es del tipo correcto en la funcion",self.linea))
                                        return 
                                
                                #VALIDAR QUE NO SE HAYA GUARDADO
                                validacion_existe = ambito_funcion.variable_existe(nombre_var)
                                if(validacion_existe == True):
                                    ast.escribir_en_consola("ERROR: La variable "+str(nombre_var)+"se inserto mas de 1 vez\n")
                                    ast.insertar_error_semantico(ERROR_LSS("SEMANTICO","EXEC: La variable "+str(nombre_var)+" se inserto mas de 1 vez",self.linea))
                                    return
                                var.modificar_valor(valor_variable)
                                ambito_funcion.agregar_variable_tabla(var)
                                print("AGREGUE VARIABLE")

                    elif(isinstance(objeto_valor_variable,Expresion)):
                        valor_variable = objeto_valor_variable.obtener_valor(actual,globa,ast)
                        #print(valor_variable)
                        var = parametros_funcion[i]
                        #print(var)
                        if(isinstance(var,VARIABLE)):
                            nombre_var = var.obtener_nombre()
                            tipo_var = var.obtener_tipo()
                            tipo_valor = objeto_valor_variable.tipo.obtener_tipo_dato()
                            #print(tipo_var)
                            #print(tipo_valor)

                            #VALIDACION TIPOS
                            if(tipo_var != tipo_valor):
                                if((tipo_var== TIPO.INT and tipo_valor == TIPO.BIT)or ((tipo_var == TIPO.NCHAR or tipo_var == TIPO.NVARCHAR)and(tipo_valor== TIPO.NCHAR or tipo_valor == TIPO.NVARCHAR) )):
                                    pass
                                else:
                                    ast.escribir_en_consola("ERROR: El valor "+str(valor_variable)+" no es del tipo correcto en la funcion\n")
                                    ast.insertar_error_semantico(ERROR_LSS("SEMANTICO","EXEC: El valor "+str(valor_variable)+" no es del tipo correcto en la funcion",self.linea))
                                    return 
                            
                            var.modificar_valor(valor_variable)
                            ambito_funcion.agregar_variable_tabla(nombre_var,var)          
                    else:
                        print("ERROR")
                #EJECUTAR CADA INSTRUCCION
                for instr in instrucciones_funcion:
                    if isinstance(instr,Instruccion):
                        instr.ejecutar(ambito_funcion,globa,ast)
                        #VALIDAR SI ACABA DE EJECUTAR UN RETURN
                        if(isinstance(instr, RETURN)):
                            self.ejecuto_return = instr.ejecuto_return  #OBTENGO LO QUE RETORNA
                            #COMPARAMOS ESTE RETURN CON EL TIPO QUE DEBE RETORNAR
                            valor_return = self.ejecuto_return.obtener_valor(ambito_funcion,globa,ast)
                            tipo_return = self.ejecuto_return.tipo.obtener_tipo_dato()
                            
                            #COMPARAR EL TIPO RETORNO CON EL RETORNO DE LA FUNCION
                            if((tipo_retorno == tipo_return) or((tipo_retorno == "BIT" or tipo_retorno == "INT") and(tipo_return=="BIT" or tipo_return =="INT"))  ):
                                respuesta = VALOR(valor_return,tipo_return,self.linea,self.columna)
                                self.tipo = respuesta.tipo
                                return valor_return
                            else:
                                #ES ERROR PORQUE NO RETORNA EL TIPO QUE DICE
                                ast.escribir_en_consola("ERROR: Funcion retorna Valor de tipo Incorrecto!\n")
                                ast.insertar_error_semantico(ERROR_LSS("SEMANTICO","FUNCION: Funcion retorna valor de tipo incorrecto",self.linea))
                                respuesta = VALOR("ERROR",TIPO.ERROR,self.linea,self.columna)
                                self.tipo = respuesta.tipo
                                return "ERROR"

                    elif(isinstance(instr, Expresion)):                 #SI EN EL ARBOL APARECE UNA EXPRESION SOLO ASI, DA IGUAL EL VALOR PORQUE ASI SE HIZO EN EL IDE
                        instr.obtener_valor(ambito_funcion,globa,ast)     # ES DECIR QUE SOLO ESCRIBIERON 1+1 Y NO LO ASIGNARON A ALGUNA VARIABLE
                
                #SALIO DEL FOR Y NO RETORNO NADA
                ast.escribir_en_consola("ERROR: Funcion no retorno valor!\n")
                ast.insertar_error_semantico(ERROR_LSS("SEMANTICO","FUNCION: No retorno valor",self.linea))
                respuesta = VALOR("ERROR",TIPO.ERROR,self.linea,self.columna)
                self.tipo = respuesta.tipo
                return "ERROR"

                                        