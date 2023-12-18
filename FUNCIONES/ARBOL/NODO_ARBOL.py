import random

class NODO_ARBOL:
    def __init__(self,nombre,linea,color):
        self.id = random.randint(10**5, 10**10)
        self.nombre = nombre
        self.linea = linea
        self.color = color
        self.hijos = []     #SOLO TENDRA DENTRO OBJETOS NODO_ARBOL

    def obtener_grafica_nodos(self):
        salida = 'n'+str(self.id) +'[label="' + str(self.nombre)+'" color="'+str(self.color)+'"];\n'
        for i in range (len(self.hijos)):
            hijo = self.hijos[i]
            if(isinstance(hijo,NODO_ARBOL)):
                salida += hijo.obtener_grafica_nodos()
                salida += 'n'+str(self.id)+' -> n'+ str(hijo.id)+'; \n'
        return salida
    
    def agregar_hijo(self,nodo):
        if(isinstance(nodo,NODO_ARBOL)):
            self.hijos.append(nodo)
        else:
            print("NODO_ARBOL: NO ES UN OBJETO NODO_ARBOL!")