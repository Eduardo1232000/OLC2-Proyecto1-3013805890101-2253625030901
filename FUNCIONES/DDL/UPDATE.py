from FUNCIONES.ARBOL.EJECUCION import *
from FUNCIONES.ARBOL.VALOR import *
from FUNCIONES.ARBOL.AST import *
from FUNCIONES.INSERTAR_BASE import *
from FUNCIONES.ERROR_LSS import *


class UPDATE(Instruccion):
    def __init__(self, tabla, set_list, col, expr, linea, columna):
        super().__init__(linea, columna, "UPDATE")
        self.tabla = tabla #ES UN VALOR
        self.set_list = set_list #ES UNA LISTA
        self.column = col #ES UN VALOR
        self.expr = expr # es un valor

    def ejecutar(self, actual, globa, ast):
        if(isinstance(self.tabla, Expresion) and isinstance(ast, AST)):
            
            base_activa = ast.obtener_base_activa()
            if(base_activa == ""):
                ast.escribir_en_consola("ERROR: No hay una DB seleccionada! \n")
                ast.insertar_error_semantico(ERROR_LSS("SEMANTICO","INSERT: No hay una base de datos seleccionada",self.linea))
                return
            
            nombre_tabla = self.tabla.obtener_valor(actual, globa, ast)
            lista_set = self.set_list #LISTA DE PARAMETROS A EVALUAR PARA CAMBIAR
            #lista_condiciones = self.condiciones
            nombre_col = self.column.obtener_valor(actual, globa, ast) # COLUMNA DE LA CONDICION A CAMBIAR
            valor_condicion = self.expr.obtener_valor(actual, globa, ast) # VALOR ACTUAL DE LA CONDICION A CAMBIAR

            ruta = "BASE_DATOS/" +str(base_activa)+".xml"

            #VALIDACION DE QUE LA TABLA EXISTE
            tree = ET.parse(ruta)
            root = tree.getroot()

            tabla_existente = False

            for base in root.findall('base'):
                if base.attrib['name'] == base_activa:
                    for tabla in base:
                        nombre = tabla.attrib['name']
                        if nombre == nombre_tabla:
                            tabla_existente = True

                            # OBTENCION DE COLUMNAS
                            for campo in tabla.findall('campo'):
                                nombre_campo = campo.find('nombre').text

                                for set_item in lista_set:
                                    if nombre_campo == set_item[0].obtener_valor(actual, globa, ast):
                                        print(f"Nombre del campo: {nombre_campo}")
                                        nuevo_valor = set_item[2].obtener_valor(actual, globa, ast)
                                        print(f"nuevo Valor {nuevo_valor}")

                                        # Buscar el índice de la columna de la condición
                                        indice_condicion = next(i for i, campo in enumerate(tabla.findall('campo')) if campo.find('nombre').text == nombre_col)

                                        # Iterar sobre los datos y actualizar el valor en la posición correspondiente
                                        for dato in tabla.findall('dato'):
                                            if dato.findall('valor')[indice_condicion].text == str(valor_condicion):
                                                dato.findall('valor')[tabla.findall('campo').index(campo)].text = str(nuevo_valor)

                            tree.write(ruta, xml_declaration=True)
                            break

                    if not tabla_existente:
                        ast.escribir_en_consola(f"ERROR: La tabla {nombre_tabla} no existe en la base: {base_activa}\n")
                        ast.insertar_error_semantico(ERROR_LSS("SEMANTICO",
                                                            f"UPDATE: La tabla {nombre_tabla} no existe en la base: {base_activa}",
                                                            self.linea))
                        return