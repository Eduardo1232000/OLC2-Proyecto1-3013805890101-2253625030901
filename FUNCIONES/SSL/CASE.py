from FUNCIONES.ARBOL.EJECUCION import *
from FUNCIONES.ARBOL.VALOR import *
from FUNCIONES.ERROR_LSS import *
from FUNCIONES.ARBOL.TABLA_FUNCIONES_VARIABLES import *
from FUNCIONES.SSL.RETURN import *
import xml.etree.ElementTree as ET

class EXP_CASE(Expresion):        
    def __init__(self,lista_whens,exp_else,linea, columna):
        super().__init__(linea, columna, "CASE")
        self.lista_whens = lista_whens
        self.exp_else = exp_else

    def obtener_valor(self, actual, globa, ast):
        #print(self.text)
        condicion_else = self.exp_else.obtener_valor(actual,globa,ast)
        tipo_else = self.exp_else.tipo


        #---------------------------------------------------------------------------------------------------------------------
        #SE USAN COLUMNAS
        base_activa = ast.obtener_base_activa()
        ruta = "BASE_DATOS/"+str(base_activa)+".xml"
        tabla_activa = ast.obtener_tabla_activa()
        if(tabla_activa !=None):
            #ast.escribir_en_consola("SE RETORNARA UNA LISTA PARA EL SELECT DE LA TABLA "+str(tabla_activa)+"\n")
            obj_tabla = self.obtener_objeto_tabla(ruta,tabla_activa)
            if(obj_tabla !=None):
                resp_lista = []
                resp_lista.append(str(tabla_activa))
                resp_lista.append("CAST")
                lista_res = []
                contador =-1
                for dato in obj_tabla.findall("dato"):
                    contador+=1
                    lista_res.append(str(condicion_else))
                for when in self.lista_whens:
                    condicion = when[0].obtener_valor(actual,globa,ast)                   
                    condicion_true = when[1].obtener_valor(actual,globa,ast)
                    for validacion in condicion:
                        if(validacion[0] == tabla_activa):
                            for num in validacion[2]:
                                lista_res[int(num)] = str(condicion_true)
                
                self.tipo = TIPODATO(TIPO.EXPRESION_SELECT)
                resp_lista.append(lista_res)
                #print(resp_lista)
                return resp_lista
            pass

            #---------------------------------------------------------------------------------------------------------------------





        for when in self.lista_whens:
            condicion = when[0].obtener_valor(actual,globa,ast)
            #print(condicion)
            
            condicion_true = when[1].obtener_valor(actual,globa,ast)  
            if(str(condicion) == str(1)):
                self.tipo = when[1].tipo
                return condicion_true
        self.tipo = tipo_else
        return condicion_else
    
    def obtener_objeto_tabla(self,ruta,nomtabla):
        tree = ET.parse(ruta)
        root = tree.getroot()
        for base in root.findall('base'):
            for tabla in base.findall('tabla'):
                if(tabla.attrib['name'] == nomtabla):
                    return tabla
        return None
    
    def obtener_lista_datos(self,objeto_tabla,nomcampo):
        lst_res = []
        lst_prin = []
        lst_prin.append(objeto_tabla.attrib['name'])
        lst_prin.append(nomcampo)
        contador =-1
        val = False
        for campos in objeto_tabla.findall('campo'):
            contador +=1
            if(campos[0].text == nomcampo):
                val = True
                break
        if(val == True):
            for dato in objeto_tabla.findall('dato'):
                lst_res.append(dato[contador].text)
        else:
            return None
        lst_prin.append(lst_res)
        return lst_prin             #[nombre_tabla, nombre_campo ,[valor,valor]]
    
class INS_CASE(Instruccion):
    def __init__(self,lista_whens,exp_else, linea, columna):
        super().__init__(linea, columna, "CASE")
        self.lista_whens = lista_whens
        self.exp_else = exp_else
        
    def ejecutar(self, actual, globa, ast):
        condicion_else = self.exp_else
        ejecuto_when = False
        for when in self.lista_whens:
            condicion = when[0].obtener_valor(actual,globa,ast)
            condicion_true = when[1]
            ambito_case = TABLA_FUNCIONES_Y_VARIABLES(actual,"CASE")
            if(str(condicion) == str(1)):
                #ast.escribir_en_consola("CUMPLE UN WHEN EJECUTAR INSTRUCCIONES")
                for instr in condicion_true:
                    if(isinstance(instr,Instruccion)):
                        instr.ejecutar(ambito_case,globa,ast)
                        
                        if(isinstance(instr, RETURN) or (instr.ejecuto_return != None)):        #VALIDAR SI HAY RETURN
                            self.ejecuto_return = instr.ejecuto_return  #OBTENGO LO QUE RETORNA

                    elif(isinstance(instr,Expresion)):
                        instr.obtener_valor(ambito_case,globa,ast)
                
                ejecuto_when = True
            if(ejecuto_when == True):
                break
        if(ejecuto_when == False):
            #ast.escribir_en_consola("SE VA A EJECUTAR EL ELSE")
            for instr in condicion_else:
                    if(isinstance(instr,Instruccion)):
                        instr.ejecutar(ambito_case,globa,ast)
                        
                        if(isinstance(instr, RETURN) or (instr.ejecuto_return != None)):        #VALIDAR SI HAY RETURN
                            self.ejecuto_return = instr.ejecuto_return  #OBTENGO LO QUE RETORNA

                    elif(isinstance(instr,Expresion)):
                        instr.obtener_valor(ambito_case,globa,ast)
