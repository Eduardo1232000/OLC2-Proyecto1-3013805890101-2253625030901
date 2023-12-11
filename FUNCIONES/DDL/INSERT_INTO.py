from FUNCIONES.ARBOL.EJECUCION import *
from FUNCIONES.ARBOL.VALOR import *
from FUNCIONES.ARBOL.AST import *
from FUNCIONES.INSERTAR_BASE import *

class INSERT_INTO(Instruccion):        
    def __init__(self,nombre,columnas,valores, linea, columna):
        super().__init__(linea, columna, "INSERT INTO ")
        self.nombre = nombre     #ES UN VALOR
        self.columnas = columnas #ES UNA LISTA
        self.valores = valores   #ES UNA LISTA

    def ejecutar(self, actual, globa, ast):
        if(isinstance(self.nombre,VALOR) and isinstance(ast, AST)):
            base_activa = ast.obtener_base_activa()
            if(base_activa == ""):  #SI NO EXISTE LA BASE
                ast.escribir_en_consola("ERROR: No hay una base de datos seleccionada!\n")
                return
            nombre_tabla = self.nombre.obtener_valor(actual,globa,ast)
            lista_columnas = self.columnas
            lista_valores = self.valores
            lista_tipos_columna = []
            lista_nombres_valor = []
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
                            break
                    if tabla_existente == True:
                        break
            if(tabla_existente == False):   #SI NO EXISTE LA TABLA
                ast.escribir_en_consola("ERROR: La Tabla "+str(nombre_tabla) +" no existe en la base "+str(base_activa)+"!\n")
                return
            if(tabla != ""):
                for campo in tabla:
                    if(campo.tag == "campo"):
                        lst = []
                        nombre = campo[0].text
                        tipo = campo[1].text
                        lst.append(nombre)
                        lst.append(tipo)
                        lista_tipos_columna.append(lst)

            #VALIDACION ORDEN COLUMNAS
            for i in range(len(lista_columnas)):
                dato_columna = lista_columnas[i]
                if(isinstance(dato_columna,VALOR)):
                    nom = dato_columna.obtener_valor(actual,globa,ast)
                    dato_columna = lista_tipos_columna[i]
                    dato_columna = dato_columna[0]
                    if(str(nom) != str(dato_columna)):  #NO ESTAN ORDENADAS LAS TABLAS
                        ast.escribir_en_consola("ERROR: El orden de las columnas no es el correcto\n")
                        return
            
            #VALIDACION TIPO DE VALOR
            #try:
            for i in range(len(lista_valores)):
                dato_valor = lista_valores[i]
                if(isinstance(dato_valor,VALOR)):
                    nom = dato_valor.obtener_valor(actual,globa,ast)
                    tipo = dato_valor.tipo.tipo
                    dato_columna = lista_tipos_columna[i]
                    dato_columna = dato_columna[1]                        
                    if((dato_columna == "INT" and (tipo == TIPO.INT or tipo == TIPO.BIT)) or (dato_columna == "BIT" and tipo == TIPO.BIT) or (dato_columna == "DECIMAL" and tipo == TIPO.DECIMAL) or(dato_columna == "DATE" and tipo == TIPO.DATE) or (dato_columna == "DATETIME" and tipo == TIPO.DATETIME) or ("VARCHAR" in dato_columna and (tipo == TIPO.VARCHAR or tipo == TIPO.CHAR))):
                        print("",end="")
                    elif("CHAR" in dato_columna and (tipo == TIPO.VARCHAR or tipo == TIPO.CHAR)):
                        inicio_parentesis = dato_columna.find('(')
                        fin_parentesis = dato_columna.find(')')
                        if inicio_parentesis != -1 and fin_parentesis != -1 and inicio_parentesis < fin_parentesis:
                            numero = int(dato_columna[inicio_parentesis + 1:fin_parentesis])
                            nuevo_nom = ""
                            if(len(nom)> numero):
                                for i in range(numero):
                                    nuevo_nom = nuevo_nom + nom[i]
                                nom = nuevo_nom
                    else:   #ALGUN TIPO DE VALOR NO ES EL CORRECTO
                        ast.escribir_en_consola("ERROR: Los tipos de los valores no coinciden con los de la tabla\n")
                        return
                    lista_nombres_valor.append(str(nom))
            #AGREGAR DATO A LA BASE
            base_agregar_dato(str(base_activa),str(nombre_tabla),lista_nombres_valor)
            ast.escribir_en_consola(" Dato Insertado! \n")
            #except:
            #    ast.escribir_en_consola("ERROR: Un tipo de dato no coincide con el tipo")