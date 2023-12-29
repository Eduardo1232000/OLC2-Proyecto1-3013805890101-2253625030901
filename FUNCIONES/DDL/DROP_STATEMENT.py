from FUNCIONES.ARBOL.EJECUCION import *
from FUNCIONES.ARBOL.VALOR import *
from FUNCIONES.BORRAR import *
from FUNCIONES.ARBOL.AST import *
from FUNCIONES.ERROR_LSS import *


class DROP_STATEMENT(Instruccion):
    def __init__(self, drop_type, nombre, linea, columna):
        super().__init__(linea, columna, "DROP STATEMENT")
        self.drop_type = drop_type #FUNCTION o PROCEDURE
        self.nombre = nombre


    def ejecutar(self, actual, globa, ast):
        if isinstance(ast, AST):
            base_activa = ast.obtener_base_activa()
            nombre_objeto = self.nombre

            if isinstance(nombre_objeto, Expresion):
                nombre = nombre_objeto.obtener_valor(actual, globa, ast)
                if self.drop_type == 'FUNCTION':
                    borrar_funcion(nombre, base_activa, ast)
                elif self.drop_type == 'PROCEDURE':
                    borrar_procedimiento(nombre, base_activa, ast)
                else:
                    ast.escribir_en_consola("("+str(self.linea)+")"+"Error: DROP no valido: " + str(self.drop_type))
                    ast.insertar_error_semantico(ERROR_LSS("SEMANTICO", "DROP: DROP No valido!", self.linea))

        else:
                ast.escribir_en_consola("("+str(self.linea)+")"+"Error: Nombre de objeto no valido")
                ast.insertar_error_semantico(ERROR_LSS("SEMANTICO", "DROP: Nombre de objeto no valido", self.linea))