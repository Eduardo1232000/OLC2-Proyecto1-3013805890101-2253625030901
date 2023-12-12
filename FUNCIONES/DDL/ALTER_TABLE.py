from FUNCIONES.ARBOL.EJECUCION import *
from FUNCIONES.ARBOL.VALOR import *
from FUNCIONES.ARBOL.AST import *
from FUNCIONES.ALTERAR_TABLA import *

class ALTER_TABLE(Instruccion):
    def __init__(self, nombre, alter_type,  linea, columna):
        super().__init__(linea, columna, "ALTER TABLE")
        self.alter_type = alter_type #ADD, DROP
        self.nombre = nombre
        

    def ejecutar(self, actual, globa, ast):
        print("DEBUG: Entrando a la función ejecutar de ALTER_TABLE")
        print("DEBUG: Tipo de alteración:", self.alter_type)
        print("DEBUG: Nombre de la tabla:", self.nombre)
        
        if isinstance(ast, AST):
            base_activa = ast.obtener_base_activa()
            nombre_tabla = self.nombre

            if isinstance(nombre_tabla, VALOR):
                nombre_tabla_valor = nombre_tabla.obtener_valor(actual, globa, ast)
                acciones = self.acciones

                if self.alter_type == 'ADD':
                    print("DEBUG: Realizando acción ADD en la tabla", nombre_tabla_valor)
                    ast.escribir_en_consola("funcionara el Alter TAble")
                
                elif self.alter_type == 'DROP':
                    print('DROP')
                elif self.alter_type == 'MODIFY':
                    print('MODIFY')
                
                else:
                    ast.escribir_en_consola("Error: ALTER TABLE incorrecto")

            else:
                ast.escribir_en_consola("Error: TABLA no valida")