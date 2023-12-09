import xml.etree.ElementTree as ET
from tkinter import simpledialog
import xml.dom.minidom
import os

def crear_base_vacia(nombre):

    #VALIDACION DE QUE EXISTE EL ARCHIVO
    if os.path.exists("BASE_DATOS/"+str(nombre) +".xml"):   #SI YA EXISTE LA BASE DE DATOS
        return False
    else:

        doc = xml.dom.minidom.Document()

        database = doc.createElement("database")
        doc.appendChild(database)    

        base = doc.createElement("base")
        base.setAttribute("name", str(nombre))

        database.appendChild(base)

        xml_con_formato = doc.toprettyxml(indent="\t")

        with open("BASE_DATOS/"+str(nombre)+".xml", "w") as archivo:
            archivo.write(xml_con_formato)
            return True