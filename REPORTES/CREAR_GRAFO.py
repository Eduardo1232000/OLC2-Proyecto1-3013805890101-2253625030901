import os
import sys

def crear_grafo(codigo,nombre):
    #print(nombre)
    
    dott = open(str(nombre)+".dot",'w')
    dott.write(codigo)
    dott.close()

    os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz/bin'
    os.system('dot -Tpng '+str(nombre)+'.dot -o '+str(nombre)+'.png')
    #os.startfile(str(nombre)+'.png')
