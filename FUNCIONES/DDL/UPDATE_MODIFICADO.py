from FUNCIONES.ARBOL.EJECUCION import *
from FUNCIONES.ARBOL.VALOR import *
from FUNCIONES.ARBOL.AST import *
from FUNCIONES.INSERTAR_BASE import *
from FUNCIONES.ERROR_LSS import *

class UPDATE_MODIFICADO(Instruccion):
    def __init__(self, tabla, set_list, where, linea, columna):
        super().__init__(linea, columna, "UPDATE")
        self.tabla = tabla #ES UN VALOR
        self.set_list = set_list #ES UNA LISTA
        self.where = where #ES UNA EXPRESION 

    def ejecutar(self, actual, globa, ast):
        #print(self.text)
        if(isinstance(self.tabla, Expresion) and isinstance(ast, AST)):
            base_activa = ast.obtener_base_activa()
            ruta = "BASE_DATOS/" +str(base_activa)+".xml"
            if(base_activa == "" or base_activa == None):
                ast.escribir_en_consola("("+str(self.linea)+")"+"ERROR: No hay una DB seleccionada! \n")
                ast.insertar_error_semantico(ERROR_LSS("SEMANTICO","INSERT: No hay una base de datos seleccionada",self.linea))
                return
            nombre_tabla = self.tabla.obtener_valor(actual, globa, ast)
            lista_set = self.set_list #LISTA DE PARAMETROS A EVALUAR PARA CAMBIAR
            ast.usar_tabla(nombre_tabla)
            validacion_where = self.where.obtener_valor(actual,globa,ast)
            posiciones_modificar = []
            for validaciones in validacion_where:
                if(validaciones[0] == nombre_tabla):
                    posiciones_modificar = validaciones[2]
                    break 
            obj_tabla = None
            tree = ET.parse(ruta)
            root = tree.getroot()
            for base in root.findall('base'):
                for tabla in base:
                    if nombre_tabla == tabla.attrib['name']:
                        obj_tabla = tabla
                        break
                if(obj_tabla != None):
                    break
            if(obj_tabla == None):
                ast.escribir_en_consola("ERROR: La tabla"+str(nombre_tabla)+ "no existe en la base: "+str(base_activa)+"\n")
                ast.insertar_error_semantico(ERROR_LSS("SEMANTICO","UPDATE: La tabla "+str(nombre_tabla)+" no existe en la base: "+str(base_activa),self.linea))
                return
            for set in lista_set:       #RECORRER LA LISTA DE SET PARA ENCONTRAR LA COLUMNA ACTUAL
                columna_actual = set[0].obtener_valor(actual,globa,ast)
                valor = set[2].obtener_valor(actual,globa,ast)
                posicion_col = self.buscar_pos_column(obj_tabla,columna_actual)
                #print("POSICION DE COLUMNA: "+str(columna_actual) +" = "+str(posicion_col)+", con update = "+str(valor))
                if(posicion_col != None):
                    contador = -1
                    for val in obj_tabla.findall("dato"):
                        contador +=1
                        if(contador in posiciones_modificar):
                            val[posicion_col].text = str(valor)
            tree.write(ruta, xml_declaration=True)
            ast.escribir_en_consola(f"UPDATE: valores actualizados satisfactoriamente en la tabla {nombre_tabla}\n")
            return
        
    def buscar_pos_column(self,obj_tabla, nombre_column):
        contador = -1
        for col in obj_tabla.findall("campo"):
            contador +=1
            if(col[0].text == nombre_column):
                return contador
        return None