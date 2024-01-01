from FUNCIONES.ARBOL.EJECUCION import *
from FUNCIONES.ARBOL.VALOR import *
from FUNCIONES.ARBOL.AST import *
from FUNCIONES.INSERTAR_BASE import *
from FUNCIONES.ERROR_LSS import *

class DELETE_MODIFICADO(Instruccion):
    def __init__(self, tabla, condicion, linea, columna):
        super().__init__(linea, columna, "DELETE")
        self.tabla = tabla  # ES UN VALOR
        self.condicion = condicion  # ES UNA EXPRESION OPCIONAL

    def ejecutar(self, actual, globa, ast):
        #print(self.text)
        if isinstance(self.tabla, Expresion) and isinstance(ast, AST):
            base_activa = ast.obtener_base_activa()
            ruta = "BASE_DATOS/" + str(base_activa) + ".xml"
            if (base_activa == "" or base_activa is None):
                ast.escribir_en_consola("(" + str(self.linea) + ")" + "ERROR: No hay una DB seleccionada! \n")
                ast.insertar_error_semantico(ERROR_LSS("SEMANTICO","DELETE: No hay una base de datos seleccionada",self.linea,))
                return

            nombre_tabla = self.tabla.obtener_valor(actual, globa, ast)
            ast.usar_tabla(nombre_tabla)

            # Obtener la condición si existe
            condicion_where = None
            if self.condicion:
                condicion_where = self.condicion.obtener_valor(actual, globa, ast)
                print(f"CONDICIONES WHERE: {condicion_where}")

            # Obtener la posición de la tabla en el XML
            obj_tabla = None
            tree = ET.parse(ruta)
            root = tree.getroot()
            for base in root.findall("base"):
                for tabla in base:
                    if nombre_tabla == tabla.attrib["name"]:
                        obj_tabla = tabla
                        break
                if obj_tabla is not None:
                    break

            if obj_tabla is None:
                ast.escribir_en_consola("ERROR: La tabla"+ str(nombre_tabla)+ "no existe en la base: "+ str(base_activa)+ "\n")
                ast.insertar_error_semantico( ERROR_LSS("SEMANTICO","DELETE: La tabla " + str(nombre_tabla)+ " no existe en la base: "+ str(base_activa),self.linea,))
                return

            # Filtrar las filas que cumplen con la condición
            posiciones_eliminar = self.filtrar_filas(obj_tabla, condicion_where)
            #ast.escribir_en_consola(f"posiciones_eliminar {posiciones_eliminar}")


            # Guardar los cambios en el XML
            tree.write(ruta, xml_declaration=True)

            ast.escribir_en_consola(f"DELETE: filas eliminadas satisfactoriamente en la tabla {nombre_tabla}\n" )
            return



    def filtrar_filas(self, obj_tabla, condicion_where):
        if condicion_where:
            posiciones_eliminar = []
            for validaciones in condicion_where:
                if validaciones[0] == obj_tabla.attrib["name"]:
                    posiciones_validar = validaciones[2]
                    posiciones_eliminar.extend(posiciones_validar)

            # Obtener la lista de elementos <dato>
            datos_a_eliminar = obj_tabla.findall("dato")

            # Obtener la lista de posiciones de los elementos <dato> que cumplen con la condición
            posiciones_datos_eliminar = sorted(posiciones_eliminar, reverse=True)

            # Eliminar las filas <dato> específicas según las posiciones indicadas por la condición
            #print("ANTES DE ELIMINAR")
            #print(ET.tostring(obj_tabla, encoding="unicode"))
            for posicion_eliminar in posiciones_datos_eliminar:
                if 0 <= posicion_eliminar < len(datos_a_eliminar):
                    dato_a_eliminar = datos_a_eliminar[posicion_eliminar]
                    obj_tabla.remove(dato_a_eliminar)

            #print("Después de la eliminación:")
            #print(ET.tostring(obj_tabla, encoding="unicode"))

            return posiciones_eliminar
        else:
            # Si la condición WHERE es None, eliminar todos los datos
            for dato_element in obj_tabla.findall("dato"):
                obj_tabla.remove(dato_element)

            #print("Después de la eliminación:")
            #print(ET.tostring(obj_tabla, encoding="unicode"))

            return list(range(len(obj_tabla.findall("dato"))))
