from FUNCIONES.ARBOL.EJECUCION import *
from FUNCIONES.ARBOL.VALOR import *
from FUNCIONES.ARBOL.AST import *
from FUNCIONES.INSERTAR_BASE import *
from FUNCIONES.ERROR_LSS import *

class DELETE(Instruccion):
    def __init__(self, tabla, condiciones, linea, columna):
        super().__init__(linea, columna, DELETE)
        self.tabla = tabla  # un valor
        self.condiciones = condiciones  # puede ser una tupla para las condiciones

    def ejecutar(self, actual, globa, ast):
        if isinstance(self.tabla, Expresion) and isinstance(ast, AST):
            base_activa = ast.obtener_base_activa()

            if base_activa == "":
                ast.escribir_en_consola("("+str(self.linea)+")"+"ERROR: No hay una BASE DE DATOS seleccionada!\n")
                ast.insertar_error_semantico(ERROR_LSS("SEMANTICO", "DELETE: No hay una base de datos seleccionada", self.linea))
                return

            nombre_tabla = self.tabla.obtener_valor(actual, globa, ast)
            condiciones = self.condiciones

            print(f"NOMBRE DE LA TABLA: {nombre_tabla}")

            ruta = "BASE_DATOS/" + str(base_activa) + ".xml"

            # VALIDAR SI LA TABLA EXISTE
            tree = ET.parse(ruta)
            root = tree.getroot()

            tabla_existente = False

            for base in root.findall('base'):
                if base.attrib['name'] == base_activa:
                    for tabla in base:
                        nombre = tabla.attrib['name']
                        if nombre == nombre_tabla:
                            tabla_existente = True
                            break

            if tabla_existente:
                if condiciones is not None:
                    # Obtener indice de la columna y operador relacional
                    nombre_columna = condiciones[0].obtener_valor(actual, globa, ast)
                    operador_relacional = condiciones[1]
                    valor_condicion = condiciones[2].obtener_valor(actual, globa, ast)

                    print(f"Nombre de la columna: {nombre_columna}")
                    print(f"Operador relacional: {operador_relacional}")
                    print(f"Valor de la condición: {valor_condicion}")

                    try:
                        # Buscar el índice de la columna de la condición
                        indice_condicion = next(
                            i for i, campo in enumerate(tabla.findall('campo')) if campo.find('nombre').text == nombre_columna)

                        # Eliminar filas que cumplen con la condición
                        filas_a_eliminar = [dato for dato in tabla.findall('dato') if self.evaluar_condicion(dato, indice_condicion, operador_relacional, valor_condicion)]

                        for fila in filas_a_eliminar:
                            tabla.remove(fila)

                    except StopIteration:
                        print(f"No se encontró la columna {nombre_columna} en la tabla {nombre_tabla}")

                        tree.write(ruta, xml_declaration=True)
                        #ast.escribir_en_consola(f"DELETE: Columnas eliminadas satisfactoriamente de la tabla {nombre_tabla} con condicion
                         #                       columna {nombre_columna} {operador_relacional} {valor_condicion}\n")

                else:
                    # Si no hay condiciones, eliminar todos los valores de las columnas
                    for dato in tabla.findall('dato'):
                        tabla.remove(dato)

                tree.write(ruta, xml_declaration=True)
                ast.escribir_en_consola(f"DELETE: Todas las filas eliminadas de la tabla {nombre_tabla}\n")

            else:
                ast.escribir_en_consola(f"ERROR: la tabla {nombre_tabla} no existe en la base: {base_activa}\n")

    def evaluar_condicion(self, dato, indice_condicion, operador_relacional, valor_condicion):
        # Obtener el valor actual en la posición de la condición
        valor_actual = dato.findall('valor')[indice_condicion].text

        # Evaluar la expresión relacional
        if operador_relacional == '=':
            return valor_actual == str(valor_condicion)
        elif operador_relacional == '<':
            return valor_actual < str(valor_condicion)
        elif operador_relacional == '>':
            return valor_actual > str(valor_condicion)
        elif operador_relacional == '<=':
            return valor_actual <= str(valor_condicion)
        elif operador_relacional == '>=':
            return valor_actual >= str(valor_condicion)
        elif operador_relacional == '!=':
            return valor_actual != str(valor_condicion)
        else:
            return False
