from abc import ABC

class ListaEjecuciones(ABC):
    def __init__(self, linea, columna, nombre_in_ex):
        self.linea = linea
        self.columna = columna
        self.nombre_in_ex = nombre_in_ex