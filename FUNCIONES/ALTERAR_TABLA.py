import xml.etree.ElementTree as ET
import xml.dom.minidom
import os

def base_existe(nombre_base):
    ruta = "BASE_DATOS/"+str(nombre_base)+".xml"
    return os.path.exists(ruta)

def tabla_existe(nombre_base, nombre_tabla):
    ruta = "BASE_DATOS/"+str(nombre_base)+".xml"
    if os.path.exists(ruta):
        try:
            tree = ET.parse(ruta)
            root = tree.getroot()

            for base in root.findall('base'):
                if base.attrib['name'] == nombre_base:
                    for tabla in base:
                        if tabla.attrib['name'] == nombre_tabla:
                            return True
            return False
        except:
            return False
    return False



def columna_existe(nombre_base, nombre_tabla, nombre_columna):
    ruta = "BASE_DATOS/"+str(nombre_base)+".xml"

    if os.path.exists(ruta):
        try:
            tree = ET.parse(ruta)
            root = tree.getroot()

            for base in root.findall('base'):
                if base.attrib['name'] == nombre_base:
                    for tabla in base:
                        if tabla.attrib['name'] == nombre_tabla:
                            # Recorrer las columnas de la tabla
                            for columna in tabla.findall('campo'):
                                nombre_actual = columna.find('nombre').text
                                if nombre_actual == nombre_columna:
                                    return True

            # Si llegamos aquí, la columna no existe
            return False
        except:
            return False
    return False


def agregar_columna(
    nombre_base, nombre_tabla, nombre_columna, tipo_columna,
    size, nulo, primarykey, foreignkey, reference
):
    try:
        print(f"Llegó a agregar_columna: {nombre_base}, {nombre_tabla}, {nombre_columna}, {tipo_columna}, {size}, {nulo}, {primarykey}, {foreignkey}, {reference}")
        ruta = f"BASE_DATOS/{nombre_base}.xml"
        tree = ET.parse(ruta)
        root = tree.getroot()

        tabla_existente = None
        for base in root.findall('base'):
            if base.attrib['name'] == nombre_base:
                for tabla in base:
                    if tabla.attrib['name'] == nombre_tabla:
                        tabla_existente = tabla
                        break
                if tabla_existente is not None:
                    break

        if tabla_existente is not None:
            nuevo_campo = ET.Element('campo')

            # Nombre
            nombre_campo = ET.SubElement(nuevo_campo, 'nombre')
            nombre_campo.text = nombre_columna

            # Tipo
            tipo_campo = ET.SubElement(nuevo_campo, 'tipo', {'size': str(size)})  # Añadir el atributo 'size'
            tipo_campo.text = tipo_columna

            # Nulo
            if nulo is not None:
                nulo_campo = ET.SubElement(nuevo_campo, 'nulo')
                nulo_campo.text = str(nulo)

            # Primary Key
            if primarykey is not None:
                primarykey_campo = ET.SubElement(nuevo_campo, 'primarykey')
                primarykey_campo.text = str(primarykey)

            # Foreign Key
            if foreignkey is not None:
                foreignkey_campo = ET.SubElement(nuevo_campo, 'foreignkey')
                foreignkey_campo.text = str(foreignkey)

            # Reference
            if reference is not None:
                reference_campo = ET.SubElement(nuevo_campo, 'reference')
                reference_campo.text = reference

            # Encontrar el último campo existente
            ultima_posicion = len(tabla_existente.findall('campo'))
            # Insertar el nuevo campo después del último campo existente
            tabla_existente.insert(ultima_posicion, nuevo_campo)

            xml_string = xml.dom.minidom.parseString(ET.tostring(root)).toprettyxml(indent="    ")

            # Eliminar líneas en blanco
            lines = xml_string.split('\n')
            xml_string = '\n'.join(line for line in lines if line.strip())

            with open(ruta, 'w', encoding='utf-8') as archivo:
                archivo.write(xml_string)
                return True
        else:
            return False
    except Exception as e:
        print(f"Error al agregar columna: {e}")
        return False



def drop_columna(nombre_base, nombre_tabla, nombre_columna):
    try:
        ruta = f"BASE_DATOS/{nombre_base}.xml"
        tree = ET.parse(ruta)
        root = tree.getroot()

        tabla_existente = None
        for base in root.findall('base'):
            if base.attrib['name'] == nombre_base:
                for tabla in base:
                    if tabla.attrib['name'] == nombre_tabla:
                        tabla_existente = tabla
                        break
                if tabla_existente is not None:
                    break

        if tabla_existente is not None:
            # Buscar la columna y eliminarla
            for columna in tabla_existente.findall('campo'):
                nombre_actual = columna.find('nombre').text
                if nombre_actual == nombre_columna:
                    tabla_existente.remove(columna)
                    xml_string = xml.dom.minidom.parseString(ET.tostring(root)).toprettyxml(indent="    ")

                    # Eliminar líneas en blanco
                    lines = xml_string.split('\n')
                    xml_string = '\n'.join(line for line in lines if line.strip())

                    with open(ruta, 'w', encoding='utf-8') as archivo:
                        archivo.write(xml_string)
                    return True

            # Si llegamos aquí, la columna no existe
            return False
        else:
            return False
    except Exception as e:
        print(f"Error al eliminar columna: {e}")
        return False


        
def modificar_tabla_xml(nombre_base, nombre_tabla, nueva_columna):
    try:
        ruta = "BASE_DATOS/"+str(nombre_base)+".xml"
        tree = ET.parse(ruta)
        root = tree.getroot()

        base_existente = None
        for base in root.findall('base'):
            if base.attrib['name'] == nombre_base:
                for tabla in base:
                    if tabla.attrib['name'] == nombre_tabla:
                        base_existente = tabla
                        break
                if base_existente is not None:
                    break

        if base_existente is not None:
            nuevo_campo = ET.SubElement(base_existente, 'campo')
            dato_campo = ET.SubElement(nuevo_campo, 'nombre')
            dato_campo.text = nueva_columna["nombre"]

            dato_campo = ET.SubElement(nuevo_campo, 'tipo')
            dato_campo.text = nueva_columna["tipo"]

            # Añadir lógica para otros atributos como 'nulo', 'primarykey', 'foreignkey', 'reference' si es necesario
            # ...

            xml_string = xml.dom.minidom.parseString(ET.tostring(root)).toprettyxml(indent="    ")

            # Eliminar líneas en blanco
            lines = xml_string.split('\n')
            xml_string = '\n'.join(line for line in lines if line.strip())

            with open(ruta, 'w', encoding='utf-8') as archivo:
                archivo.write(xml_string)
                return True

        else:
            return False
    except:
        return False 