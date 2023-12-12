from FUNCIONES.ARBOL.EJECUCION import *
from FUNCIONES.ARBOL.VALOR import *
from FUNCIONES.ARBOL.AST import *
from FUNCIONES.ALTERAR_TABLA import *

class ALTER_TABLE(Instruccion):
    def __init__(self, alter_type, nombre, acciones, linea, columna):
        super().__init__(linea, columna, "ALTER TABLE")
        self.alter_type - alter_type #ADD, DROP
        self.nombre = nombre
        self.acciones = acciones

    def ejecutar(self, actual, globa, ast):
        if isinstance(ast, AST):
            base_activa = ast.obtener_base_activa()
            nombre_tabla = self.nombre

            if isinstance(nombre_tabla, VALOR):
                nombre_tabla_valor = nombre_tabla.obtener_valor(actual, globa, ast)
                acciones = self.acciones

                if self.alter_type == 'ADD':
                    alter_table_add(base_activa, nombre_tabla_valor, acciones, ast)
                
                elif self.alter_type == 'DROP':
                    print('DROP')
                elif self.alter_type == 'MODIFY':
                    print('MODIFY')
                
                else:
                    ast.escribir_en_consola("Error: ALTER TABLE incorrecto")

            else:
                ast.escribir_en_consola("Error: TABLA no valida")