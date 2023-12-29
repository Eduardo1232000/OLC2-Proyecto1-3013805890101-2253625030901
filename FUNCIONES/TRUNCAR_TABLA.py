import xml.etree.ElementTree as ET
import xml.dom.minidom
import os

def truncate_table(nombre_base, nombre_tabla, ast):
    try:
        
        ruta = f"BASE_DATOS/{nombre_base}.xml"
        tree = ET.parse(ruta)
        root = tree.getroot()

        tabla_existente = None
        for base in root.findall('base'):
            for tabla in base:
                if tabla.attrib['name'] == nombre_tabla:
                    tabla_existente = tabla
                    break
                if tabla_existente is not None:
                    break
                
        
            if tabla_existente is not None:
                #eliminar todos los registros da la tabla
                llave_primaria = None
                for campo in tabla_existente.findall('campo'):
                    if campo.find('primarykey').text == 'true':
                        llave_primaria = campo.find('nombre').text
                        break

            if llave_primaria is not None:
                # Verificar si la llave primaria se utiliza como llave foránea en otras tablas
                referencia_en_otras_tablas = False
                for base in root.findall('base'):
                    for tabla in base:
                        for campo in tabla.findall('campo'):
                            referencia = campo.find('reference')
                            if referencia is not None and referencia.text == llave_primaria:
                                referencia_en_otras_tablas = True
                                break
                        if referencia_en_otras_tablas:
                            break
                    if referencia_en_otras_tablas:
                        break

                if referencia_en_otras_tablas:
                    #print("No se pueden eliminar los datos de la tabla debido a restricciones de integridad referencial.")
                    ast.escribir_en_consola(f"No se pueden eliminar los datos de la tabla:  {nombre_tabla}  debido a restricciones de integridad referencial.")
                    return False
                
            for dato in tabla_existente.findall('dato'):
                tabla_existente.remove(dato)
            #tabla_existente.remove(tabla_existente.find('registro'))

            xml_string = xml.dom.minidom.parseString(ET.tostring(root)).toprettyxml(indent="    ")

            #eliminar lineas en blanco
            lines = xml_string.split('\n')
            xml_string = '\n'.join(line for line in lines if line.strip())

            with open(ruta, 'w', encoding='utf-8') as archivo:
                archivo.write(xml_string)
                return True
        
        else:
            return False
    except Exception as e:
        ast.escribir_en_consola(f"Error al truncar la tabla: {e}")
        return False