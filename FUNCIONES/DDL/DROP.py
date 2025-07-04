from FUNCIONES.ARBOL.EJECUCION import *
from FUNCIONES.ARBOL.VALOR import *
from FUNCIONES.BORRAR import *
from FUNCIONES.ARBOL.AST import *
from FUNCIONES.ERROR_LSS import *

class DROP(Instruccion):
    def __init__(self, drop_type, nombre, linea, columna):
        super().__init__(linea, columna, "DROP")
        self.drop_type = drop_type.upper()  # DATA BASE o TABLE
        self.nombre = nombre

    def ejecutar(self, actual, globa, ast):
        if isinstance(ast, AST):
            base_activa = ast.obtener_base_activa()
            nombre_objeto = self.nombre

            if isinstance(nombre_objeto, Expresion):
                nombre = nombre_objeto.obtener_valor(actual, globa, ast)
                if self.drop_type == 'TABLE':
                    # Accede al nombre de la base de datos actual a través de base_activa
                    #aqui debería de existir una instruccion para ver si hay una foreign key que haga relacion 
                    nombre_base_actual = base_activa
                    borrar_tabla(nombre, nombre_base_actual, ast)
                elif self.drop_type == 'DATA':
                    borrar_base(nombre, ast)
                else:
                    ast.escribir_en_consola("("+str(self.linea)+")"+"Error: DROP no valido: " + str(self.drop_type))
                    ast.insertar_error_semantico(ERROR_LSS("SEMANTICO","DROP: DROP No valido!",self.linea))
            else:
                ast.escribir_en_consola("("+str(self.linea)+")"+"Error: Nombre de objeto no valido")
                ast.insertar_error_semantico(ERROR_LSS("SEMANTICO","DROP: Nombre de objeto no valido",self.linea))

                
