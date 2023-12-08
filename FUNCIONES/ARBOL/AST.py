from FUNCIONES.ARBOL.EJECUCION import *
class AST:
    def __init__(self, ejecuciones):
        self.EJECUCIONES = ejecuciones   #LISTADO DE OBJETOS PARA EJECUTAR
        self.salida_cadena = ""  #SALIDA DE TEXTO QUE SE MUESTRA EN CONSOLA
        self.codigo_grafica=""   #CODIGO DE GRAPHVIZ DEL ARBOL
        self.tabla_simbolos=[]   #TABLA DE SIMBOLOS DEL CODIGO
    
    def ejecutar(self):
        for instr in self.EJECUCIONES:

            if isinstance(instr,Instruccion):
                instr.ejecutar("actual","global",self)


            elif(isinstance(instr, Expresion)):                 #SI EN EL ARBOL APARECE UNA EXPRESION SOLO ASI, DA IGUAL EL VALOR PORQUE ASI SE HIZO EN EL IDE
                instr.obtener_valor("actual","global",self)     # ES DECIR QUE SOLO ESCRIBIERON 1+1 Y NO LO ASIGNARON A ALGUNA VARIABLE

        #YA DEBE TENER LAS RESPUESTAS DE CADA OPERACION 
        print(self.salida_cadena)   #BORRAR SI NO SE QUIERE VER LAS RESPUESTAS DE CONSOLA

    def escribir_en_consola(self,texto):    #ESCRIBIR EN LA CONSOLA
        self.salida_cadena += str(texto)

    def obtener_salida(self):
        return(self.salida_cadena)
    
    def graficar(nodos):
        print("NO IMPLEMENTADO")

    def guardar_en_tabla_simbolos(identificador,tipo_variable, tipo, entorno,linea,columna):
        print("NO IMPLEMENTADO")
    
    def graficar_tabla_simbolos():
        print("NO IMPLEMENTADO")

    def graficar_reporte_errores(lista_errores):
        print("NO IMPLEMENTADO")