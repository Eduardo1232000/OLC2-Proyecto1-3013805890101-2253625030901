from FUNCIONES.ARBOL.EJECUCION import *
from FUNCIONES.ARBOL.VALOR import *
from FUNCIONES.CREAR_BASE import *
from FUNCIONES.ARBOL.TABLA_FUNCIONES_VARIABLES import *
from FUNCIONES.ARBOL.AST import *
from FUNCIONES.ERROR_LSS import *
from FUNCIONES.ALTERAR_PROCEDURE import *

import xml.etree.ElementTree as ET
import xml.dom.minidom

class ALTER_FUNCTION_BASE(Instruccion):
    def __init__(self, nombre, retorno, tipo_v, lista_variables, lista_instruccion, linea, columna):
        super().__init__(linea, columna, "ALTER FUNCTION")
        self.nombre = nombre    # VALOR
        self.tipo = tipo_v      # STRING
        self.retorno = retorno
        self.lista_variables = lista_variables  # LISTA NOMBRES DE VARIABLES A GUARDAR
        self.lista_instruccion = lista_instruccion  # LISTA DE OBJETOS INSTRUCCION O EXPRESION

    def ejecutar(self, actual, globa, ast):
        nombre_base = ast.obtener_base_activa()
        if nombre_base == "":
            ast.escribir_en_consola("ERROR: No hay una base activa\n")
            ast.insertar_error_semantico(ERROR_LSS("SEMANTICO", "ALTER: No hay una base activa", self.linea))
            return

        nombre_func = self.nombre.obtener_valor(actual, globa, ast)
        tipo_retorno = self.retorno.obtener_tipo_dato()
        size_tipo_retorno = self.retorno.obtener_size()
        lista_parametros = []

        if self.lista_variables is not None:
            for var in self.lista_variables:
                if isinstance(var[0], Expresion) and isinstance(var[1], TIPODATO):
                    nombre_variable = var[0].obtener_valor(actual, globa, ast)
                    if var[1].tipo == TIPO.INT:
                        tipo_var = "INT"
                        size_tipo_var = 0
                    elif var[1].tipo == TIPO.DECIMAL:
                        tipo_var = "DECIMAL"
                        size_tipo_var = 0
                    elif var[1].tipo == TIPO.DATE:
                        tipo_var = "DATE"
                        size_tipo_var = 0
                    elif var[1].tipo == TIPO.DATETIME:
                        tipo_var = "DATETIME"
                        size_tipo_var = 0
                    elif var[1].tipo == TIPO.NCHAR:
                        tipo_var = "NCHAR"
                        if isinstance(var[1], TIPODATO):
                            size_tipo_var = var[1].obtener_size()
                    elif var[1].tipo == TIPO.NVARCHAR:
                        tipo_var = "NVARCHAR"
                        if isinstance(var[1], TIPODATO):
                            size_tipo_var = var[1].obtener_size()
                    else:
                        tipo_var = "ERROR"
                        ast.escribir_en_consola("ERROR: No se reconoció un tipo de dato\n")
                        ast.insertar_error_semantico(ERROR_LSS("SEMANTICO", "ALTER: No se reconoció un tipo de dato", self.linea))
                        return

                    lst = []
                    lst.append(nombre_variable)
                    lst.append(tipo_var)
                    lst.append(size_tipo_var)
                    lista_parametros.append(lst)

        # MODIFICAR LA FUNCIÓN EN LA BASE
        ruta = "BASE_DATOS/" + str(nombre_base) + ".xml"
        tree = ET.parse(ruta)
        root = tree.getroot()

        for base in root.findall('base'):
            for funcion in base.findall('funcion'):
                if funcion.attrib['name'] == nombre_func:
                    # Modificar la información de retorno
                    retorno_element = funcion.find('retorno')
                    retorno_element.set('type', str(tipo_retorno))
                    retorno_element.set('size', str(size_tipo_retorno))

                    # Modificar la información de parámetros
                    parameters_element = funcion.find('parameters')
                    if parameters_element is not None:
                        funcion.remove(parameters_element)

                    if len(lista_parametros) != 0:
                        nuevo_parameters = ET.SubElement(funcion, 'parameters')
                        for param in lista_parametros:
                            nuevo_param = ET.SubElement(nuevo_parameters, 'parameter')
                            nuevo_param.set('name', str(param[0]))
                            nuevo_param.set('type', str(param[1]))
                            nuevo_param.set('size', str(param[2]))

                    # Modificar las sentencias
                    sentencias_element = funcion.find('sentencias')
                    if sentencias_element is not None:
                        funcion.remove(sentencias_element)

                    nuevo_sentencias = ET.SubElement(funcion, 'sentencias')
                    for sent in self.lista_instruccion[0]:
                        nuevo_sent = ET.SubElement(nuevo_sentencias, 'sentencia')
                        nuevo_sent.text = sent.text

                    xml_string = xml.dom.minidom.parseString(ET.tostring(root)).toprettyxml(indent="    ")

                    # Eliminar líneas en blanco
                    lines = xml_string.split('\n')
                    xml_string = '\n'.join(line for line in lines if line.strip())

                    with open(ruta, 'w', encoding='utf-8') as archivo:
                        archivo.write(xml_string)

                    ast.escribir_en_consola("FUNCION ALTERADA\n")
                    return

        ast.escribir_en_consola("ERROR: No se encontró la función para alterar\n")
        ast.insertar_error_semantico(ERROR_LSS("SEMANTICO", "ALTER: No se encontró la función para alterar", self.linea))

