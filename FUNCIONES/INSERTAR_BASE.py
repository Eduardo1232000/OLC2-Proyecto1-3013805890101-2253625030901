
import xml.etree.ElementTree as ET
import xml.dom.minidom
import os

def base_agregar_tabla(nombre_base, nombre_tabla):
    try:
        ruta = "BASE_DATOS/"+str(nombre_base)+".xml"
        tree = ET.parse(ruta)
        root = tree.getroot()

        base_existente = None
        for base in root.findall('base'):
            if base.attrib['name'] == nombre_base:
                base_existente = base
                break

        if base_existente is not None:
            nueva_tabla = ET.SubElement(base_existente, 'tabla')
            nueva_tabla.set('name', nombre_tabla)
                    
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

def base_agregar_campo(nombre_base, nombre_tabla,nombre_campo,tipo_campo,nulo,primarykey,foreignkey,reference,columna):
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
            dato_campo.text = nombre_campo

            dato_campo = ET.SubElement(nuevo_campo, 'tipo')
            dato_campo.set('size', str(columna))

            dato_campo.text = tipo_campo

            dato_campo = ET.SubElement(nuevo_campo, 'nulo')
            dato_campo.text = nulo

            dato_campo = ET.SubElement(nuevo_campo, 'primarykey')
            dato_campo.text = primarykey

            dato_campo = ET.SubElement(nuevo_campo, 'foreignkey')
            dato_campo.text = foreignkey

            dato_campo = ET.SubElement(nuevo_campo, 'reference')
            dato_campo.text = reference

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

def base_agregar_dato(nombre_base,nombre_tabla,valores):
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
            nuevo_campo = ET.SubElement(base_existente, 'dato')
            for valor in valores:
                dato_campo = ET.SubElement(nuevo_campo, 'valor')
                dato_campo.text = str(valor)


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
    
def validar_existe_tabla(nombre_base, nombre_tabla):
    ruta = "BASE_DATOS/"+str(nombre_base)+".xml"
    if os.path.exists(ruta):   #SI YA EXISTE LA BASE DE DATOS
        return False
    
#PRUEBAS
#base_agregar_tabla("Alimentos","comidas")
#base_agregar_tabla("Personas","Hombres")
#base_agregar_tabla("Personas","Mujeres")
#base_agregar_tabla("Alimentos","personas")
#base_agregar_campo("Alimentos","comidas","id_comida","int","false","true","false","false")
#base_agregar_campo("Alimentos","comidas","id_comida","nchar(100)","false","true","false","false")
#base_agregar_campo("Personas","Hombres","id_hombre","int","false","true","false","false")
#base_agregar_campo("Personas","Hombres","nombre","nchar(100)","false","false","false","false")
'''lista = []
lista.append("1")
lista.append("Pera")
lista.append("1")

base_agregar_dato("Alimentos", "products",lista)'''

