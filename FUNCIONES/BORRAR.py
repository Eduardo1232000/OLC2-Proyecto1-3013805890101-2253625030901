import os
import xml.etree.ElementTree as ET
import xml.dom.minidom

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
        ruta = os.path.join("BASE_DATOS", f"{nombre_base}.xml")

        if not os.path.exists(ruta):
            ast.escribir_en_consola(f"Error: La base de datos '{nombre_base}' no existe.")
            return False

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
                    # Verificar dependencias
                    llave_primaria = None
                    for campo in tabla_existente.findall('campo'):
                        if campo.find('primarykey') is not None and campo.find('primarykey').text.lower() == 'true':
                            llave_primaria = campo.find('nombre').text
                            break

                    if llave_primaria is not None:
                        # Verificar si la llave primaria se utiliza como llave foránea en otras tablas
                        referencia_en_otras_tablas = False
                        for base_otra_tabla in root.findall('base'):
                            for otra_tabla in base_otra_tabla.findall('tabla'):
                                for campo_otra_tabla in otra_tabla.findall('campo'):
                                    referencia = campo_otra_tabla.find('reference')
                                    if referencia is not None and referencia.text == llave_primaria:
                                        referencia_en_otras_tablas = True
                                        break
                                if referencia_en_otras_tablas:
                                    break
                            if referencia_en_otras_tablas:
                                break

                        if referencia_en_otras_tablas:
                            ast.escribir_en_consola(f"No se pueden eliminar la tabla '{nombre_tabla}' debido a restricciones de integridad referencial.")
                            return False

                    # Borrar la tabla
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

    except FileNotFoundError:
        ast.escribir_en_consola(f"Error: No se pudo encontrar la base de datos '{nombre_base}'.")
        return False
    except ET.ParseError:
        ast.escribir_en_consola(f"Error: No se pudo parsear el archivo XML de la base de datos '{nombre_base}'.")
        return False
    except Exception as e:
        ast.escribir_en_consola(f"Error al intentar eliminar la tabla '{nombre_tabla}': {e}")
        return False


def borrar_funcion(nombre_funcion, nombre_base, ast):
    try:
        ruta = "BASE_DATOS/" + str(nombre_base) + ".xml"
        tree = ET.parse(ruta)
        root = tree.getroot()

        funcion_existente = None
        for base in root.findall('base'):
            if base.attrib['name'] == nombre_base:
                for funcion in base.findall('funcion'):
                    if funcion.attrib['name'] == nombre_funcion:
                        funcion_existente = funcion
                        break
                if funcion_existente is not None:
                    base.remove(funcion_existente)

                    xml_string = xml.dom.minidom.parseString(ET.tostring(root)).toprettyxml(indent="    ")

                    # Eliminar líneas en blanco
                    lines = xml_string.split('\n')
                    xml_string = '\n'.join(line for line in lines if line.strip())

                    with open(ruta, 'w', encoding='utf-8') as archivo:
                        archivo.write(xml_string)

                    ast.escribir_en_consola(f"Función '{nombre_funcion}' en la base de datos '{nombre_base}' eliminada correctamente.")
                    return True

        ast.escribir_en_consola(f"Error: La función '{nombre_funcion}' no existe en la base de datos '{nombre_base}'.")
        return False
    except Exception as e:
        ast.escribir_en_consola(f"Error al intentar eliminar la función '{nombre_funcion}': {e}")
        return False


    
def borrar_procedimiento(nombre_procedure, nombre_base, ast):
    try:
        ruta = "BASE_DATOS/" + str(nombre_base) + ".xml"
        tree = ET.parse(ruta)
        root = tree.getroot()

        procedure_existente = None
        for base in root.findall('base'):
            if base.attrib['name'] == nombre_base:
                for procedure in base.findall('procedure'):
                    if procedure.attrib['name'] == nombre_procedure:
                        procedure_existente = procedure
                        break
                if procedure_existente is not None:
                    base.remove(procedure_existente)

                    xml_string = xml.dom.minidom.parseString(ET.tostring(root)).toprettyxml(indent="    ")

                    # Eliminar líneas en blanco
                    lines = xml_string.split('\n')
                    xml_string = '\n'.join(line for line in lines if line.strip())

                    with open(ruta, 'w', encoding='utf-8') as archivo:
                        archivo.write(xml_string)

                    ast.escribir_en_consola(f"Procedimiento '{nombre_procedure}' en la base de datos '{nombre_base}' eliminado correctamente.")
                    return True

        ast.escribir_en_consola(f"Error: El procedimiento '{nombre_procedure}' no existe en la base de datos '{nombre_base}'.")
        return False
    except Exception as e:
        ast.escribir_en_consola(f"Error al intentar eliminar el procedimiento '{nombre_procedure}': {e}")
        return False
