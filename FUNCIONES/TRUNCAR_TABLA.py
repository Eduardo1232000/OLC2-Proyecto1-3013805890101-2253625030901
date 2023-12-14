import xml.etree.ElementTree as ET
import xml.dom.minidom
import os

def truncate_table(nombre_base, nombre_tabla):
    try:
        print(nombre_base + " <-- NOMBRE DE LA base")
        print("Nombre de la tabla: " + nombre_tabla)
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
        print(f"Error al truncar la tabla: {e}")
        return False