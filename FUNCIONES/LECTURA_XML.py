import xml.etree.ElementTree as ET
import os

def construir_estructura_arbol_xml():
    #LEER CADA BASE DE DATOS
    try:
        nombres_archivos = os.listdir('BASE_DATOS/')
    except OSError as e:
        nombres_archivos = None
        print(f"No se pudo acceder a la carpeta de base de datos: {e}")

    if nombres_archivos:
        bases = []
        for nombre_archivo in nombres_archivos:
            ruta = "BASE_DATOS/"+str(nombre_archivo)
            #print(nombre_archivo)
            tree = ET.parse(ruta)
            root = tree.getroot()
            lista_base = []
            lista_tablas= []
            lista_funciones = []
            lista_procedimientos = []
            
            for base in root.findall('base'):
                #print(base.get('name'))#NOMBRE DE LA BASE
                lista_base.append(str(base.get('name')))
                for dato in base:
                    if(dato.tag == "tabla"):
                        #print("\t"+dato.get('name'))
                        lista_tablas.append(str(dato.get('name')))
                    elif(dato.tag == "funcion"):
                        lista_funciones.append(str(dato.get('name')))
                    elif(dato.tag == "procedimiento"):
                        lista_procedimientos.append(str(dato.get('name')))
                lista_base.append(lista_tablas)
                lista_base.append(lista_funciones)
                lista_base.append(lista_procedimientos)

                
            bases.append(lista_base)
        return bases