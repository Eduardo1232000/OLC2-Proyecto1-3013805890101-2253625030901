from FUNCIONES.ARBOL.EJECUCION import *
from FUNCIONES.ARBOL.VALOR import *
from FUNCIONES.CREAR_BASE import *
from FUNCIONES.ARBOL.TABLA_FUNCIONES_VARIABLES import *
from FUNCIONES.ARBOL.AST import *
from FUNCIONES.ERROR_LSS import *
from FUNCIONES.ALTERAR_PROCEDURE import *



class ALTER_PROCEDURE_BASE(Instruccion):
    def __init__(self, nombre, tipo_v, lista_variables, lista_instruccion, linea, columna):
        super().__init__(linea, columna, "ALTER_PROCEDURE")
        self.nombre = nombre
        self.tipo = tipo_v
        self.lista_variables = lista_variables
        self.lista_instruccion = lista_instruccion

    def ejecutar(self, actual, globa, ast):
        if (
            isinstance(actual, TABLA_FUNCIONES_Y_VARIABLES)
            and isinstance(globa, TABLA_FUNCIONES_Y_VARIABLES)
            and isinstance(ast, AST)
            and isinstance(self.nombre, Expresion)
        ):

            nombre_base = ast.obtener_base_activa()
            nombre_func = self.nombre.obtener_valor(actual, globa, ast)
            lista_parametros = []

            if self.lista_variables is not None:
                # Hay lista de variables, procesarla
                for var in self.lista_variables:
                    if (
                        isinstance(var[0], Expresion)
                        and isinstance(var[1], TIPODATO)
                    ):
                        nombre_variable = var[0].obtener_valor(actual, globa, ast)
                        tipo_var = None
                        size_tipo_var = None

                        if var[1].tipo == TIPO.INT:
                            tipo_var = "INT"
                            size_tipo_var = 0
                        elif var[1].tipo == TIPO.DECIMAL:
                            tipo_var = "DECIMAL"
                            size_tipo_var = 0
                        elif var[1].tipo == TIPO.DATE:
                            tipo_var = "DATE"
                            size_tipo_var = 0
                        elif var[1].tipo == TIPO.DATETIME:
                            tipo_var = "DATETIME"
                            size_tipo_var = 0
                        elif var[1].tipo == TIPO.NCHAR:
                            tipo_var = "NCHAR"
                            if isinstance(var[1], TIPODATO):
                                size_tipo_var = var[1].obtener_size()
                        elif var[1].tipo == TIPO.NVARCHAR:
                            tipo_var = "NVARCHAR"
                            if isinstance(var[1], TIPODATO):
                                size_tipo_var = var[1].obtener_size()
                        else:
                            tipo_var = "ERROR"
                            ast.escribir_en_consola(
                                "("+str(self.linea)+")"+"ERROR: No se reconoció un tipo de dato"
                            )
                            ast.insertar_error_semantico(
                                ERROR_LSS(
                                    "SEMANTICO",
                                    "ALTER: No se reconoció un tipo de dato ",
                                    self.linea,
                                )
                            )
                            return

                        lst = []
                        lst.append(nombre_variable)
                        lst.append(tipo_var)
                        lst.append(size_tipo_var)
                        lista_parametros.append(lst)

            # Procesar la lista de instrucciones (sentencias)
            lista_sentencias = []
            for sentencia in self.lista_instruccion[0]:
                lista_sentencias.append(sentencia.text)

            # Imprimir información para verificar
            print(f"nombre_base: {nombre_base}")
            print(f"nombre_func: {nombre_func}")
            print(f"nombre_lista_par: {lista_parametros}")
            print(f"nombre_lista_fun: {lista_sentencias}")

            # Luego, puedes utilizar lista_parametros y lista_sentencias según tu lógica
            agregar_o_modificar_procedure(
                nombre_base, nombre_func, lista_parametros, lista_sentencias, ast)


    
                        
