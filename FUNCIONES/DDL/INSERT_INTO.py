from FUNCIONES.ARBOL.EJECUCION import *
from FUNCIONES.ARBOL.VALOR import *
from FUNCIONES.ARBOL.AST import *
from FUNCIONES.INSERTAR_BASE import *
from FUNCIONES.ERROR_LSS import *

class INSERT_INTO(Instruccion):        
    def __init__(self,nombre,columnas,valores, linea, columna):
        super().__init__(linea, columna, "INSERT INTO ")
        self.nombre = nombre     #ES UN VALOR
        self.columnas = columnas #ES UNA LISTA
        self.valores = valores   #ES UNA LISTA

    def ejecutar(self, actual, globa, ast):
        #print(self.text)
        if(isinstance(self.nombre,Expresion) and isinstance(ast, AST)):
            base_activa = ast.obtener_base_activa()
            if(base_activa == ""):  #SI NO EXISTE LA BASE
                ast.escribir_en_consola("ERROR: No hay una base de datos seleccionada!\n")
                ast.insertar_error_semantico(ERROR_LSS("SEMANTICO","INSERT: No hay una base de datos seleccionada",self.linea))
                return
            nombre_tabla = self.nombre.obtener_valor(actual,globa,ast)
            lista_columnas = self.columnas
            lista_valores = self.valores

            lista_nombres_valor = []

            lst_nombre = []
            lst_tipo = []
            lst_nulo = []
            lst_foreign = []
            lst_reference = []
            ruta = "BASE_DATOS/"+str(base_activa)+".xml"

            #VALIDACION QUE EXISTA LA TABLA
            tree = ET.parse(ruta)
            root = tree.getroot()
            tabla_existente = False
            for base in root.findall('base'):
                if base.attrib['name'] == base_activa:
                    for tabla in base:
                        nombre = str(tabla.attrib['name'])
                        if nombre == nombre_tabla:
                            tabla_existente = True
                            #OBTENCION DE COLUMNAS
                            for campo in tabla.findall('campo'):            #RECORRE CADA CAMPO Y AGREGA A CADA LISTA SU DATO
                                for dato in campo.findall('nombre'):
                                    lst_nombre.append(dato.text)

                                for dato in campo.findall('tipo'):  #TIPO
                                    lst_tipo.append(dato.text)

                                for dato in campo.findall('nulo'):  #NULO
                                    lst_nulo.append(dato.text)

                                for dato in campo.findall('foreignkey'):  #FOREIGN
                                    lst_foreign.append(dato.text)
                                
                                for dato in campo.findall('reference'):  #REFERENCE
                                    lst_reference.append(dato.text)
                            break
                    if tabla_existente == True:
                        break

            if(tabla_existente == False):   #SI NO EXISTE LA TABLA
                ast.escribir_en_consola("ERROR: La Tabla "+str(nombre_tabla) +" no existe en la base "+str(base_activa)+"!\n")
                ast.insertar_error_semantico(ERROR_LSS("SEMANTICO","INSERT: La tabla "+str(nombre_tabla) +" no existe en la base "+str(base_activa),self.linea))
                return
            
            '''#COLUMNAS TABLA
            print(lst_nombre)
            print(lst_tipo)
            print(lst_nulo)
            print(lst_foreign)
            print(lst_reference)

            print(lista_columnas)'''




            #VALIDACION ORDEN COLUMNAS
            if(len(lista_columnas)> len(lst_nombre)):
                ast.escribir_en_consola("ERROR: El numero de columnas es mayor a la de la tabla")
                ast.insertar_error_semantico(ERROR_LSS("SEMANTICO","INSERT: El numero de columnas es mayor a la de la tabla!",self.linea))
                return
            
            if(len(lista_columnas) != len(lista_valores)):
                ast.escribir_en_consola("ERROR: El numero de datos no coincide al numero de columnas")
                ast.insertar_error_semantico(ERROR_LSS("SEMANTICO","INSERT: El numero de datos no coincide al numero de columnas!",self.linea))
                return
            
            
            avanza = 0
            for i in range(len(lst_nombre)):            #RECORRE LAS COLUMNAS
                nombre_columna = lst_nombre[i]
                tipo_columna = lst_tipo[i]
                nulo_columna = lst_nulo[i]
                foreign_columna = lst_foreign[i]
                reference_columna = lst_reference[i]

                if((i-avanza) <= (len(lista_columnas)-1)):
                    valor_columna = lista_columnas[i - avanza]

                    valor_insertar = lista_valores[i - avanza]

                    if(isinstance(valor_columna,Expresion) and isinstance(valor_insertar,Expresion)):
                        nombre_columna_insert = valor_columna.obtener_valor(actual,globa,ast)
                        valor_dato = valor_insertar.obtener_valor(actual,globa,ast)
                        tipo_valor_dato = valor_insertar.tipo.tipo
                        #print(nombre_columna_insert)
                        #print(valor_dato)
                        #print("---")

                        
                        if(nombre_columna_insert == nombre_columna):    #CUMPLE CON EL ORDEN
                            #VALIDAR SI ES FOREIGN KEY Y VALIDAR LA REFERENCIA
                            encontre_ref = False
                            encontre_valor_ref = False
                            if(foreign_columna != "false"):
                                
                                print("validar referencia")
                                for base in root.findall('base'):
                                    contador = -1
                                    for tabla in base:
                                        nombre = str(tabla.attrib['name'])
                                        contador +=1
                                        print("AUMENTA CONTADOR: "+str(contador)+" , "+str(nombre)+",  "+str(foreign_columna))
                                        if nombre == foreign_columna:
                                            #VALIDAR EXISTE EL CAMPO DE REFERENCIA
                                            contador = -1
                                            for campo in tabla:
                                                if(campo.tag == "campo"):
                                                    #print("CAMPO")
                                                    contador +=1
                                                    if(encontre_ref == True):
                                                        contador-=1
                                                        continue
                                                    nombre_campo = campo[0].text
                                                    if(nombre_campo == reference_columna):
                                                        print("LO ENCONTRE EL CAMPO DE REFERENCIA"+str(nombre_campo)+" "+str(reference_columna)+str(contador))
                                                        encontre_ref = True
                                                elif(campo.tag == "dato"):
                                                    print("DATO "+str(contador))
                                                    print(repr(campo[contador].text) + repr(valor_dato))
                                                    print("")
                                                    if(encontre_ref == False):
                                                        ast.escribir_en_consola("ERROR: No existe el campo de referencia")
                                                        ast.insertar_error_semantico(ERROR_LSS("SEMANTICO","INSERT: No existe el campo de referencia",self.linea))
                                                        return
                                                    if(str(campo[contador].text) == str(valor_dato)):
                                                        encontre_valor_ref = True
                                                        print("ENCOTRADO")
                                print(encontre_valor_ref)                    #for valor in campo:
                                if(encontre_valor_ref == False):
                                    ast.escribir_en_consola("ERROR: El valor no existe en la referencia\n")
                                    ast.insertar_error_semantico(ERROR_LSS("SEMANTICO","INSERT: El valor no existe en la referencia",self.linea))
                                    return

                            #VALIDAR QUE EL PRIMARY KEY NO SE REPITA


                            
                            #FIN VALIDACION





                            #VALIDAR EL TIPO DEL VALOR

                            if((tipo_columna == "INT" and (tipo_valor_dato == TIPO.INT or tipo_valor_dato == TIPO.BIT)) or (tipo_columna == "BIT" and tipo_valor_dato == TIPO.BIT) or (tipo_columna == "DECIMAL" and tipo_valor_dato == TIPO.DECIMAL) or(tipo_columna == "DATE" and tipo_valor_dato == TIPO.DATE) or (tipo_columna == "DATETIME" and tipo_valor_dato == TIPO.DATETIME) or ("NVARCHAR" in tipo_columna and (tipo_valor_dato == TIPO.NVARCHAR or tipo_valor_dato == TIPO.NCHAR))):
                                print("",end="")
                            elif("NCHAR" in tipo_columna and (tipo_valor_dato == TIPO.NVARCHAR or tipo_valor_dato == TIPO.NCHAR)):
                                inicio_parentesis = tipo_columna.find('(')
                                fin_parentesis = tipo_columna.find(')')
                                if inicio_parentesis != -1 and fin_parentesis != -1 and inicio_parentesis < fin_parentesis:
                                    numero = int(tipo_columna[inicio_parentesis + 1:fin_parentesis])
                                    nuevo_nom = ""
                                    if(len(valor_dato)> numero):
                                        for i in range(numero):
                                            nuevo_nom = nuevo_nom + valor_dato[i]
                                        valor_dato = nuevo_nom
                            else:   #ALGUN TIPO DE VALOR NO ES EL CORRECTO
                                ast.escribir_en_consola("ERROR: "+str(nombre_columna)+": "+str(valor_dato)+" es de tipo incorrecto: "+str(tipo_columna)+"-"+str(tipo_valor_dato)+"\n")
                                ast.insertar_error_semantico(ERROR_LSS("SEMANTICO","INSERT:"+str(nombre_columna)+": "+str(valor_dato)+" es de tipo incorrecto: "+str(tipo_columna)+"-"+str(tipo_valor_dato),self.linea))
                                return
                            #GUARDARLO EN LA LISTA
                            lista_nombres_valor.append(valor_dato)
                            
                        else:
                            if(nulo_columna == "true"):
                                lista_nombres_valor.append("")
                            else:
                                ast.escribir_en_consola("ERROR: Se omitio una columna que no era NULL o esta mal escrita: "+str(nombre_columna)+"-"+str(nombre_columna_insert)+"\n")
                                ast.insertar_error_semantico(ERROR_LSS("SEMANTICO","INSERT: Se omitio una columna que no era NULL",self.linea))
                                return
                            avanza+=1
                            #GUARDAR UN DATO VACIO EN LA LISTA

                else:   #LAS DEMAS COLUMNAS DEBEN SER NULO O ES ERROR
                    #print("VALIDAR SI ES NULO")
                    if(nulo_columna == "true"):
                        lista_nombres_valor.append("")
                    else:
                        ast.escribir_en_consola("ERROR: Se omitio una columna que no era NULL o esta mal escrita\n")
                        ast.insertar_error_semantico(ERROR_LSS("SEMANTICO","INSERT: Se omitio una columna que no era NULL",self.linea))
                        return

             #AGREGAR DATO A LA BASE
            salida = base_agregar_dato(str(base_activa),str(nombre_tabla),lista_nombres_valor)
            if(salida == True):
                ast.escribir_en_consola(" Dato Insertado! \n")
            else:
                ast.escribir_en_consola(" ERROR AL INSERTAR \n")
                ast.insertar_error_semantico(ERROR_LSS("SEMANTICO","INSERT: Ocurrio un error al insertar",self.linea))

            