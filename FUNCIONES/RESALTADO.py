from tkinter import *
import re

def resaltar_palabras(contenido_texto):
    palabras_clave = ['select', 'from', 'where', 'as', 'create', 'table', 'data base',
                      'concatenar', 'substraer','hoy','contar','suma',
                      'cast', 'int','bit','decimal','date','datetime','nchar','nvarchar',
                      'not','null','primary key','foreign', 'reference',
                      'insert','into','values','delete']

    contenido_texto.tag_remove('palabra_clave', '1.0', 'end-1c')

    for palabra in palabras_clave:
        inicio = '1.0'
        while inicio:
            inicio = contenido_texto.search(r'\y' + re.escape(palabra) + r'\y', inicio, 'end-1c', nocase=True, regexp=True)
            if inicio:
                fin = f'{inicio}+{len(palabra)}c'
                contenido_texto.tag_add('palabra_clave', inicio, fin)
                inicio = fin

    contenido_texto.tag_configure('palabra_clave', foreground='purple', font=('Arial', 10, 'bold'))