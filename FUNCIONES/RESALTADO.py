from tkinter import *
import re

def resaltar_palabras(contenido_texto):
    palabras_clave = ['select', 'from', 'where', 'as', 'create', 'table', 'data base',
                      'concatenar', 'substraer', 'hoy', 'contar', 'suma',
                      'cast', 'int', 'bit', 'decimal', 'date', 'datetime', 'nchar', 'nvarchar',
                      'not', 'null', 'primary key', 'foreign', 'reference',
                      'insert', 'into', 'values', 'delete', 'drop', 'alter', 'update', 'truncate',
                      'PROCEDURE', 'BEGIN', 'END', 'EXEC', 'DECLARE', 'SET', 'USE',
                      ]

    contenido_texto.tag_remove('identificador', '1.0', 'end-1c')
    contenido_texto.tag_remove('palabra_clave', '1.0', 'end-1c')
    contenido_texto.tag_remove('identificador_comillas', '1.0', 'end-1c')
    contenido_texto.tag_remove('numero', '1.0', 'end-1c')

    for palabra in palabras_clave:
        inicio = '1.0'
        while inicio:
            inicio = contenido_texto.search(r'\y' + re.escape(palabra) + r'\y', inicio, 'end-1c', nocase=True, regexp=True)
            if inicio:
                fin = f'{inicio}+{len(palabra)}c'
                contenido_texto.tag_add('palabra_clave', inicio, fin)
                inicio = fin

    # Identificadores sin comillas
    identificadores = re.findall(r'\b[a-zA-Z][a-zA-Z0-9_]*\b', contenido_texto.get("1.0", "end-1c"))
    for identificador in identificadores:
        inicio = '1.0'
        while inicio:
            inicio = contenido_texto.search(r'\y' + re.escape(identificador) + r'\y', inicio, 'end-1c', nocase=True, regexp=True)
            if inicio:
                fin = f'{inicio}+{len(identificador)}c'
                contenido_texto.tag_add('identificador', inicio, fin)
                inicio = fin

    # Identificadores entre comillas
    identificadores_comillas = re.findall(r'"[a-zA-Z0-9_-]+"', contenido_texto.get("1.0", "end-1c"))
    for identificador_comillas in identificadores_comillas:
        inicio = '1.0'
        while inicio:
            inicio = contenido_texto.search(re.escape(identificador_comillas), inicio, 'end-1c', nocase=True, regexp=True)
            if inicio:
                fin = f'{inicio}+{len(identificador_comillas)}c'
                contenido_texto.tag_add('identificador_comillas', inicio, fin)
                inicio = fin

    contenido_texto.tag_configure('identificador', foreground='blue', font=('Arial', 10, 'bold'))
    contenido_texto.tag_configure('palabra_clave', foreground='purple', font=('Arial', 10, 'bold'))
    contenido_texto.tag_configure('identificador_comillas', foreground='red', font=('Arial', 10, 'bold'))
