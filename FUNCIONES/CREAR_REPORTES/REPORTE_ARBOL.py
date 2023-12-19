from FUNCIONES.ARBOL.NODO_ARBOL import *
from FUNCIONES.ARBOL.EJECUCION import *

class grafica_arbol:
    def __init__(self):
        self.izq = None
        self.der = None
        self.padre = None

    def obtener_codigo_grafica_reporte_arbol(self,lista_ejecuciones):
        codigo = "digraph AST {\n"
        codigo += 'node [shape=box, style=rounded];\n'
        nodo_principal = NODO_ARBOL("PROGRAMA",0,"red")
        self.izq = None
        self.der = None
        for i in range(len(lista_ejecuciones)):
            instr = lista_ejecuciones[i]
            if isinstance(instr,Instruccion) or isinstance(instr,Expresion):
                nodo_a = instr.nodo_arbol
                if(isinstance(nodo_a, NODO_ARBOL)):
                    self.padre = NODO_ARBOL("INSTRUCCIONES",0,"yellow")
                    if(self.izq != None):
                        self.padre.agregar_hijo(self.izq)
                    self.der = NODO_ARBOL("INSTRUCCION",0,"green")
                    self.der.agregar_hijo(nodo_a)
                    self.padre.agregar_hijo(self.der)
                    self.izq = self.padre
        if(self.izq != None):
            nodo_principal.agregar_hijo(self.izq)
        codigo += nodo_principal.obtener_grafica_nodos()
        codigo += '}\n'
        return codigo