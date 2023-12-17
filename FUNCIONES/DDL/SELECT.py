from FUNCIONES.ARBOL.EJECUCION import * 
from FUNCIONES.ARBOL.VALOR import*
from FUNCIONES.ARBOL.AST import *
from FUNCIONES.ERROR_LSS import *
from FUNCIONES.SELECCION import *

class SELECT(Instruccion):
    def __init__(self, columnas, tabla, condiciones, linea, columna):
        super().__init__(linea, columna, "SELECT")
        self.columnas = columnas  # ES UNA LISTA
        self.tabla = tabla
        print(self.tabla)
        self.condiciones = condiciones  # ES UNA LISTA

    def ejecutar(self, actual, globa, ast):
        if (isinstance(self.columnas, list) and isinstance(ast, AST)):
            base_activa = ast.obtener_base_activa()
            if base_activa == "":
                mensaje_error = "Error: No hay una base de datos seleccionada"
                ast.escribir_en_consola(mensaje_error)
                ast.insertar_error_semantico(ERROR_LSS("SEMANTICO", mensaje_error, self.linea))
                return 
            
            #lista_columnas = self.columnas.obtener_valor(actual, globa, ast)
            nombre_tabla = self.tabla.obtener_valor(actual, globa, ast)
            lista_condiciones = self.condiciones
            print("NOMBRE DE LA TABLA: " + nombre_tabla)

            mensaje_ejecucion = f"SELECT: Base activa: {base_activa}, Tabla: {nombre_tabla}, Columnas: {self.columnas}"
            ast.escribir_en_consola(mensaje_ejecucion)

            resultado = seleccionar_datos(base_activa, nombre_tabla, self.columnas)
            
            if isinstance(resultado, tuple):
                campos, datos = resultado
                mensaje_resultado = f"Campos: {campos}\nDatos:\n{', '.join(map(str, datos))}"
                ast.escribir_en_consola(mensaje_resultado)
            else:
                ast.escribir_en_consola(resultado)
            




            

