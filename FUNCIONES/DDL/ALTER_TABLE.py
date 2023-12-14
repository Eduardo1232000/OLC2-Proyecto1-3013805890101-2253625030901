from FUNCIONES.ARBOL.EJECUCION import *
from FUNCIONES.ARBOL.VALOR import *
from FUNCIONES.ARBOL.AST import *
from FUNCIONES.CREAR_BASE import *
from FUNCIONES.ALTERAR_TABLA import *

class ALTER_TABLE(Instruccion):        
    def __init__(self, nombre_tabla, operacion, linea, columna):
        super().__init__(linea, columna, "ALTER TABLE")
        self.nombre_tabla = nombre_tabla  # ES UN VALOR
        self.operacion = operacion  # Operación específica (tupla) según la producción de la gramática
        

    def ejecutar(self, actual, globa, ast):
        if isinstance(ast, AST):
            base_activa = ast.obtener_base_activa()
            if base_activa == "":  # SI NO EXISTE LA BASE
                ast.escribir_en_consola("ERROR: No hay una base de datos seleccionada!\n")
                return

            nombre_tabla = self.nombre_tabla.obtener_valor(actual, globa, ast)

            # Aquí deberías implementar la lógica específica para cada operación de ALTER TABLE
            if self.operacion[0] == "ADD":
                self.ejecutar_add(actual, globa, ast, nombre_tabla)
            elif self.operacion[0] == "DROP":
                self.ejecutar_drop(actual, globa, ast, nombre_tabla)

    def ejecutar_add(self, actual, globa, ast, nombre_tabla):
        if self.operacion[1] == "COLUMN":
            base_activa = ast.obtener_base_activa()
            nombre_columna = self.operacion[2].obtener_valor(actual, globa, ast)
            tipo_dato = self.operacion[3]
            nombre_tipo_dato = tipo_dato.tipo

            if agregar_columna(base_activa, nombre_tabla, nombre_columna, tipo_dato.tipo, nulo=True, primarykey=False, foreignkey=False, reference=False):
                ast.escribir_en_consola(f"Se ha agregado la columna {nombre_columna} de tipo {nombre_tipo_dato} a la tabla {nombre_tabla}\n")
            else:
                ast.escribir_en_consola(f"No se pudo agregar la columna {nombre_columna} a la tabla {nombre_tabla}\n")

            #ast.escribir_en_consola(f"Se ha agregado la columna {nombre_columna} de tipo  {tipo_dato} a la tabla {nombre_tabla}\n")
        elif self.operacion[1] == "CONSTRAINT":
            # Lógica para procesar la adición de una restricción, por ejemplo, una llave foránea
            pass
        # Puedes agregar más lógica según sea necesario

    def ejecutar_drop(self, actual, globa, ast, nombre_tabla):
        if self.operacion[1] == "COLUMN":
            base_activa= ast.obtener_base_activa()
            nombre_columna = self.operacion[2].obtener_valor(actual, globa, ast)
            if drop_columna(base_activa, nombre_tabla, nombre_columna):
                ast.escribir_en_consola(f"Se ha eliminado la columna {nombre_columna} de la tabla {nombre_tabla}")
