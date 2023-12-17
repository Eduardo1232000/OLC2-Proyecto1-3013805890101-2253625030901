import xml.etree.ElementTree as ET
import xml.dom.minidom
import os

def seleccionar_datos(base_activa, tabla, columnas):
    try:
        ruta= "BASE_DATOS/" + str(base_activa)+ ".xml"
        tree = ET.parse(ruta)
        root = tree.getroot()

        tabla_existente = None
        for base in root.findall('base'):
            if base.attrib['name'] == base_activa:
                for tabla_xml in base:
                    nombre_tabla = tabla_xml.attrib['name']
                    if nombre_tabla == tabla:
                        tabla_existente = tabla_xml
                        break
                    if tabla_existente is not None:
                        break

        if tabla_existente is not None:
            if columnas == ['*']:
                campos_resultado = []
                datos_resultado = []
                for campo in tabla_existente.findall('campo'):
                    campos_resultado.append(campo.find('nombre').text)
                
                for dato in tabla_existente.findall('dato'):
                    fila_resultado = []
                    for valor in dato:
                        fila_resultado.append(valor.text)
                        datos_resultado.append(fila_resultado)

                return campos_resultado, datos_resultado
            
            else:
                    #aqui se imprime cuando manda columnas seleccionadas
                pass
        
        else:
            print(f"Error: la tabla {tabla} no existe en DB")

    except Exception as e:
        print(f"Error al ejecutar la seleccion: {e}\n")