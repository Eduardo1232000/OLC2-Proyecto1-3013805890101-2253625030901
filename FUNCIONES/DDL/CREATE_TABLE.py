from FUNCIONES.ARBOL.EJECUCION import *
from FUNCIONES.ARBOL.VALOR import *
from FUNCIONES.CREAR_BASE import *
from FUNCIONES.ARBOL.AST import *
from FUNCIONES.INSERTAR_BASE import *

class CREATE_TABLE(Instruccion):        
    def __init__(self,nombre,datos, linea, columna):
        super().__init__(linea, columna, "CREATE TABLE ")
   #SON OBJETOS VALOR
        self.nombre = nombre    #ES UN VALOR
        self.datos = datos      #ES UNA LISTA

    def ejecutar(self, actual, globa, ast):
        if(isinstance(ast,AST)):
            base_activa = ast.obtener_base_activa()
            nombre_tabla = ""
            numero_primary_keys = 0
            nombre_tabla = self.nombre.obtener_valor(actual,globa,ast)
            
            #VALIDAR QUE NO EXISTA LA TABLA
            ruta = "BASE_DATOS/"+str(base_activa)+".xml"
            tree = ET.parse(ruta)
            root = tree.getroot()
            base_existente = False
            for base in root.findall('base'):
                if base.attrib['name'] == base_activa:
                    for tabla in base:
                        nombre = str(tabla.attrib['name'])
                        if nombre == nombre_tabla:
                            base_existente = True
                            break
                    if base_existente == True:
                        break
            
            if(base_existente == True):
                ast.escribir_en_consola("ERROR: Ya existe la Tabla: "+str(nombre_tabla) +" en la Base de Datos: "+str(base_activa))
                return

            #NO EXISTE LA TABLA

            lista_campos = []
            #RECORRER LA LISTA DE CAMPOS
            for lista in self.datos:
                table = CAMPO_TABLA("","false","false","false","false","false",self.linea,self.columna)        #OBJETO TABLA VACIO
                if(isinstance(lista,FORANEA)):
                    #print("ENCONTRE UNA LLAVE FORANEA")
                    tabla_base = lista.obtener_tabla_base()
                    base_origen = lista.obtener_base_origen()
                    tabla_referencia = lista.obtener_tabla_referencia()

                    nom_tabla_base = tabla_base.obtener_valor(actual,globa,ast)
                    nom_base_origen = base_origen.obtener_valor(actual,globa,ast)
                    nom_tabla_referencia = tabla_referencia.obtener_valor(actual,globa,ast)

                    #RECORRER LA LISTA DE CAMPOS EN BUSCA DE LA TABLA BASE
                    for i in range(len(lista_campos)):
                        campo = lista_campos[i]
                        if(isinstance(campo,CAMPO_TABLA)):
                            nombre_campo = campo.obtener_valor(actual,globa,ast)

                            if(nombre_campo == nom_tabla_base):
                                campo.cambiar_foreign_key(nom_base_origen)
                                campo.cambiar_reference(nom_tabla_referencia)
                                lista_campos[i] = campo

                else: #ES UNA LISTA
                    #RECORRER LA LISTA DEL DATO [NOMBRE, TIPO, CARACTERISTICAS]
                    for dato in lista:
                        if(isinstance(dato,VALOR)):
                            nombre_campo = dato.obtener_valor(actual,globa,ast)
                            table.cambiar_nombre(nombre_campo)
                        elif(isinstance(dato,TIPODATO)):
                            #print("ES UN TIPO")
                            tipo = dato.tipo
                            size = dato.obtener_size()
                            if(dato.tipo == TIPO.CHAR):
                                tipo = dato.tipo+ "(" + str(size) + ")"
                            table.cambiar_tipo(tipo)
                            
                        else: #ES UNA LISTA DE CARACTERISTICAS
                            for caract in dato:
                                if(isinstance(caract,TIPODATO)):
                                    if(caract.tipo == TIPO.NULL):
                                        table.cambiar_nulo("true")
                                    elif(caract.tipo == TIPO.NOT_NULL):
                                        table.cambiar_nulo("false")
                                    elif(caract.tipo == TIPO.PRIMARY_KEY):
                                        table.cambiar_primary_key("true")
                                        table.cambiar_nulo("false")
                                        numero_primary_keys +=1

                    #AGREGAR EL CAMPO A LA LISTA
                    lista_campos.append(table)

            #VERIFICAR QUE NO EXISTAN 2 PRIMARY KEY
            if(numero_primary_keys>=2):
                ast.escribir_en_consola("ERROR: Hay 2 Primary Key en la tabla!")
                return

            #INSERTAR TABLA
            base_agregar_tabla(base_activa,nombre_tabla)
            #SI VIENE PRIMARY KEY ES NO NULO
            for campo in lista_campos:
                if(isinstance(campo,CAMPO_TABLA)):
                    nombre_campo = campo.obtener_valor(actual,globa,ast)
                    tipo = campo.obtener_tipo()
                    nulo = campo.obtener_nulo()
                    primary_key = campo.obtener_primary_key()
                    foreign = campo.obtener_foreign_key()
                    reference = campo.obtener_reference()

                    base_agregar_campo(base_activa,nombre_tabla,nombre_campo,tipo,nulo,primary_key,foreign,reference)

            ast.escribir_en_consola("TABLA CREADA!")
