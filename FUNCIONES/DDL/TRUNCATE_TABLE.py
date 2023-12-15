from FUNCIONES.ARBOL.EJECUCION import *

from FUNCIONES.ARBOL.VALOR import *
from FUNCIONES.ARBOL.AST import *
from FUNCIONES.TRUNCAR_TABLA import *
from FUNCIONES.ERROR_LSS import *

class TRUNCATE_TABLE(Instruccion):
    def __init__(self, nombre_tabla, linea, columna):
        super().__init__(linea, columna, "TRUNCATE TABLE")
        self.nombre_tabla = nombre_tabla #VALOR
        

    def ejecutar(self, actual, globa, ast):
        print("paso a ejecutar?")
        if isinstance(ast, AST):
            base_activa = ast.obtener_base_activa()
            if base_activa == "":
                ast.escribir_en_consola("Error: No hay una base de datos seleccionada \n")
                ast.insertar_error_semantico(ERROR_LSS("SEMANTICO","TRUNCATE: No hay una base de datos seleccionada",self.linea))
                return
                
            nombre_tabla = self.nombre_tabla.obtener_valor(actual, globa, ast)
            

            if truncate_table(base_activa, nombre_tabla):
                ast.escribir_en_consola(f"Se ha truncado la tabla {nombre_tabla}")
            else:
                
                ast.escribir_en_consola(f"No se pudo truncar la tabla {nombre_tabla}")
                ast.insertar_error_semantico(ERROR_LSS("SEMANTICO","TRUNCATE: No se pudo truncar la tabla",self.linea))