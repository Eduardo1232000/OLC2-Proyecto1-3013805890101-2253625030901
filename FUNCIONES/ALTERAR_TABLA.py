import xml.etree.ElementTree as ET
import xml.dom.minidom

class AST:
    def escribir_en_consola(self, mensaje):
        print(mensaje)

def alter_table_add(nombre_base, nombre_tabla, acciones, ast):
    ast.escribir_en_consola(f"alter add")

def alter_table_drop(nombre_base, nombre_tabla, acciones, ast):
    ast.escribir_en_consola(f"alter table drop")
    
def alter_table_modify(nombre_base, nombre_tabla, accionces, ast):
    ast.escribir_en_consola(f"alter table modify")