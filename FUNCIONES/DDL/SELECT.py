from FUNCIONES.ARBOL.EJECUCION import * 
from FUNCIONES.ARBOL.VALOR import*
from FUNCIONES.ARBOL.AST import *
from FUNCIONES.ERROR_LSS import *
from FUNCIONES.SELECCION import *

class SELECT(Instruccion):
    def __init__(self, columnas, name, condiciones, linea, columna):
        
        super().__init__(linea, columna, "SELECT")
        self.columnas = columnas
        self.tabla = name
        self.condiciones = condiciones        

    def ejecutar(self, actual, globa, ast):
        
        if (isinstance(self.tabla, Expresion) and isinstance(ast, AST)):
            base_activa = ast.obtener_base_activa()
            if base_activa == "":
                mensaje_error = "Error: No hay una base de datos seleccionada"
                ast.escribir_en_consola(mensaje_error)
                ast.insertar_error_semantico(ERROR_LSS("SEMANTICO", mensaje_error, self.linea))
                return
             
        

            nombre_tabla = self.tabla.obtener_valor(actual, globa, ast)
            lista_condiciones = self.condiciones
            columnas = self.columnas
            valores_condiciones = []
            
            for condicion in lista_condiciones:
                if isinstance(condicion, Expresion):
                    valor_condicion = condicion.obtener_valor(actual, globa, ast)
                    valores_condiciones.append(valor_condicion)
                else:
                    valores_condiciones.append(condicion)
            
            mensaje_ejecucion = f"SELECT: Base activa: {base_activa}, Tabla: {nombre_tabla}, Columnas: {columnas}, Condiciones: {valores_condiciones}"
            ast.escribir_en_consola(mensaje_ejecucion)
            resultado = seleccionar_datos(base_activa, nombre_tabla, self.columnas, lista_condiciones)

            
            if isinstance(resultado, tuple):
                campos, datos = resultado
                mensaje_resultado = f"Campos: {campos}\nDatos:\n{', '.join(map(str, datos))}"
                ast.escribir_en_consola(mensaje_resultado)
            else:
                ast.escribir_en_consola(resultado)
            



            

