import os
import xml.etree.ElementTree as ET
import xml.dom.minidom

class AST:
    def escribir_en_consola(self, mensaje):
        print(mensaje)

def borrar_base(nombre_base, ast):
    try:
        ruta = "BASE_DATOS/" + str(nombre_base) + ".xml"
        if os.path.exists(ruta):
            os.remove(ruta)
            ast.escribir_en_consola(f"Base de datos '{nombre_base}' eliminada correctamente.")
            return True
        else:
            ast.escribir_en_consola(f"Error: La base de datos '{nombre_base}' no existe.")
            return False
    except Exception as e:
        ast.escribir_en_consola(f"Error al intentar eliminar la base '{nombre_base}': {e}")
        return False

def borrar_tabla(nombre_tabla, nombre_base, ast):
    try:
        ruta = "BASE_DATOS/" + str(nombre_base) + ".xml"
        tree = ET.parse(ruta)
        root = tree.getroot()

        tabla_existente = None
        for base in root.findall('base'):
            if base.attrib['name'] == nombre_base:
                for tabla in base.findall('tabla'):
                    if tabla.attrib['name'] == nombre_tabla:
                        tabla_existente = tabla
                        break
                if tabla_existente is not None:
                    base.remove(tabla_existente)

                    xml_string = xml.dom.minidom.parseString(ET.tostring(root)).toprettyxml(indent="    ")

                    # Eliminar líneas en blanco
                    lines = xml_string.split('\n')
                    xml_string = '\n'.join(line for line in lines if line.strip())

                    with open(ruta, 'w', encoding='utf-8') as archivo:
                        archivo.write(xml_string)

                    ast.escribir_en_consola(f"Tabla '{nombre_tabla}' en la base de datos '{nombre_base}' eliminada correctamente.")
                    return True

        ast.escribir_en_consola(f"Error: La tabla '{nombre_tabla}' no existe en la base de datos '{nombre_base}'.")
        return False
    except Exception as e:
        ast.escribir_en_consola(f"Error al intentar eliminar la tabla '{nombre_tabla}': {e}")
        return False
