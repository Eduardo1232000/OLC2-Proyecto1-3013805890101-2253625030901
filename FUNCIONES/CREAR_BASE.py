import xml.etree.ElementTree as ET
from tkinter import simpledialog
import xml.dom.minidom

def crear_base_vacia(nombre):
    doc = xml.dom.minidom.Document()

    database = doc.createElement("database")
    doc.appendChild(database)    

    base = doc.createElement("base")
    base.setAttribute("name", str(nombre))

    database.appendChild(base)

    xml_con_formato = doc.toprettyxml(indent="\t")

    with open("BASE_DATOS/"+str(nombre)+".xml", "w") as archivo:
        archivo.write(xml_con_formato)
