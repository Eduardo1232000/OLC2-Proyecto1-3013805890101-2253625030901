import xml.etree.ElementTree as ET
import xml.dom.minidom
import os
def agregar_o_modificar_procedure(nombre_base, nombre_procedure, lista_parametros, lista_instrucciones, ast):
    ruta = "BASE_DATOS/" + str(nombre_base) + ".xml"
    tree = ET.parse(ruta)
    root = tree.getroot()

    # Buscar si ya existe un procedimiento con el mismo nombre
    procedimiento_existente = None
    for base in root.findall("base"):
        for proc in base.findall("procedure"):
            if proc.attrib["name"] == nombre_procedure:
                procedimiento_existente = proc
                break

    if procedimiento_existente is not None:
        # Modificar el procedimiento existente
        modificar_procedure(
            procedimiento_existente, lista_parametros, lista_instrucciones, ast
        )
    else:
        # Agregar un nuevo procedimiento al final de la base
        base = root.find("base[@name='" + nombre_base + "']")
        agregar_procedure(
            base, nombre_procedure, lista_parametros, lista_instrucciones, ast
        )

    # Guardar los cambios en el archivo XML
    xml_string = xml.dom.minidom.parseString(ET.tostring(root)).toprettyxml(indent="    ")
    
    # Eliminar líneas en blanco
    lines = xml_string.split('\n')
    xml_string = '\n'.join(line for line in lines if line.strip())

    with open(ruta, 'w', encoding='utf-8') as archivo:
        archivo.write(xml_string)

    ast.escribir_en_consola("SE HIZO EL CAMBIO\n")

def agregar_procedure(base, nombre_procedure, lista_parametros, lista_instrucciones, ast):
    nuevo_procedure = ET.SubElement(base, "procedure")
    nuevo_procedure.set("name", nombre_procedure)

    # Agregar parámetros ordenados
    if len(lista_parametros) != 0:
        nuevo_parameters = ET.SubElement(nuevo_procedure, "parameters")
        for param in sorted(lista_parametros, key=lambda x: x[0]):
            nuevo_param = ET.SubElement(nuevo_parameters, "parameter")
            nuevo_param.set("name", str(param[0]))
            nuevo_param.set("type", str(param[1]))
            nuevo_param.set("size", str(param[2]))

    # Agregar sentencias ordenadas
    nuevo_sentencias = ET.SubElement(nuevo_procedure, "sentencias")
    for sent in lista_instrucciones:
        nuevo_sent = ET.SubElement(nuevo_sentencias, "sentencia")
        nuevo_sent.text = sent

    ast.escribir_en_consola("AGREGAMOS UN PROCEDURE\n")

def modificar_procedure(procedure, lista_parametros, lista_instrucciones, ast):
    # Obtener o crear la sección de parameters
    parameters_existente = procedure.find(".//parameters")
    if parameters_existente is not None:
        parameters_existente.clear()
    else:
        parameters_existente = ET.SubElement(procedure, "parameters")

    # Agregar parámetros ordenados
    if len(lista_parametros) != 0:
        for param in sorted(lista_parametros, key=lambda x: x[0]):
            nuevo_param = ET.SubElement(parameters_existente, "parameter")
            nuevo_param.set("name", param[0])
            nuevo_param.set("type", param[1])
            nuevo_param.set("size", str(param[2]))

    # Obtener o crear la sección de sentencias
    sentencias_existente = procedure.find(".//sentencias")
    if sentencias_existente is not None:
        sentencias_existente.clear()
    else:
        sentencias_existente = ET.SubElement(procedure, "sentencias")

    # Agregar sentencias ordenadas
    for sent in sorted(lista_instrucciones):
        nuevo_sent = ET.SubElement(sentencias_existente, "sentencia")
        nuevo_sent.text = sent

    ast.escribir_en_consola("MODIFICAMOS UN PROCEDURE\n")

