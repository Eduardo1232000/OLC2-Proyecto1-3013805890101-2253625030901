from FUNCIONES.ARBOL.EJECUCION import * 
from FUNCIONES.ARBOL.VALOR import*
from FUNCIONES.ARBOL.AST import *
from FUNCIONES.ERROR_LSS import *
from FUNCIONES.SELECCION import *

class SELECT(Instruccion):
    def __init__(self, columnas, tablas, condiciones, linea, columna):
        
        super().__init__(linea, columna, "SELECT")
        self.columnas = columnas #LISTA
        self.tabla = tablas
        self.condiciones = condiciones #LISTA  

    def ejecutar(self, actual, globa, ast):
        
        if (isinstance(ast, AST)):
            
            base_activa = ast.obtener_base_activa()
            if base_activa == "":
                mensaje_error = "Error: No hay una base de datos seleccionada"
                ast.escribir_en_consola(mensaje_error)
                ast.insertar_error_semantico(ERROR_LSS("SEMANTICO", mensaje_error, self.linea))
                return
             
        

            #nombre_tabla = self.tabla.obtener_valor(actual, globa, ast)
            #print(f"ESTAMOS IMPRIMIENDO EL NOMBRE DE LA TABLA {self.tabla[1].obtener_valor(actual, globa, ast)}")
            lista_condiciones = self.condiciones 
            lista_columnas = self.columnas
            
            
            valores_condiciones = []
            for condicion in lista_condiciones:
                if isinstance(condicion, Expresion):
                    valor_condicion = condicion.obtener_valor(actual, globa, ast)
                    #print(f"expresion {valor_condicion}")
                    valores_condiciones.append(valor_condicion)
                else:
                    valores_condiciones.append(condicion)

            
            """
            

            valores_tablas = []
            for lista_tabla in lista_tablas:
                for tabla in lista_tabla:
                    valor_tabla = tabla.obtener_valor(actual, globa, ast)
                    valores_tablas.append(valor_tabla)        
            """
            valores_columnas = []
            for lista_columna in lista_columnas:
                for columna in lista_columna:
                    valor_columna = columna.obtener_valor(actual, globa, ast)
                    valores_columnas.append(valor_columna)
            




            #print(f"VALORES DE COLUMNAS: {valores_columnas}" )

            nombres_tablas = [tabla.obtener_valor(None, None, None) if isinstance(tabla, VALOR) else tabla for tabla in self.tabla]
            #nombres_columnas = [columna.obtener_valor(None, None, None) if isinstance(columna, VALOR) else columna for columna in self.columnas]

            
            mensaje_ejecucion = f"SELECT: Base activa: {base_activa}, Tabla: {nombres_tablas}, Columnas: {valores_columnas}, Condiciones: {valores_condiciones} \n"
            ast.escribir_en_consola(mensaje_ejecucion)
            resultado = seleccionar_datos(base_activa, nombres_tablas, valores_columnas, valores_condiciones)

            
            if isinstance(resultado, tuple):
                campos, datos = resultado
                mensaje_resultado = f"Campos: {campos}\nDatos:\n{', '.join(map(str, datos))}"
                ast.escribir_en_consola(mensaje_resultado)
            else:
                ast.escribir_en_consola(resultado)
            



            

