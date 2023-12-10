import os

def borrar_base(nombre, ast):
    directorio_base = "BASE_DATOS"
    archivo_xml = os.path.join(directorio_base, f"{nombre}.xml")

    try:
        if os.path.exists(archivo_xml):
            os.remove(archivo_xml)
            ast.escribir_en_consola(f"DATA BASE {nombre} Eliminada!\n")
        else:
            ast.escribir_en_consola(f"DATA BASE {nombre} NOT FOUND\n")
    except OSError as e:
        ast.escribir_en_consola(f"Error al intentar eliminar DATA BASE {nombre}: {e}\n")