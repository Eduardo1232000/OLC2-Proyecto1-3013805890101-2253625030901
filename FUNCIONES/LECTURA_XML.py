import xml.etree.ElementTree as ET
import os
def leer_xml(nombre_archivo):
    # Parsear el archivo XML
    tree = ET.parse(nombre_archivo)
    root = tree.getroot()
    print(root.get('name'))

    # TABLAS
    for tabla in root.findall('table'):
        nombre = tabla.get('name')
        print("TABLA: "+str(nombre))

        for columna in tabla.findall('column'):
            nombre_col = columna.get("name")
            print("\tCOLUMNA: "+str(nombre_col))

        for dato in tabla.findall('data'):
            for filas in dato.findall('row'):
                print("\tFILA")
                for valor in filas.findall('value'):
                    print("\t\t"+str(valor.text))

def construir_estructura_arbol_xml(nombre_archivo):
    tree = ET.parse(nombre_archivo)
    root = tree.getroot()
    base = []
    datos = []
    base.append(str(root.get('name')))
    # TABLAS
    for tabla in root.findall('table'):
        nombre = tabla.get('name')
        datos.append(str(tabla.get('name')))
    base.append(datos)
    base.append(datos)      #NO ESTABA LA ESTRUCTURA DE FUNCIONES
    base.append(datos)      #NO ESTABA LA ESTRUCTURA DE PROCEDIMIENTOS
    return base
