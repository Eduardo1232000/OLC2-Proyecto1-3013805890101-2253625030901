from FUNCIONES.ERROR_LSS import *

def obtener_codigo_grafica_reporte_errores(lista_errores):
    codigo = "digraph G{\n"
    codigo += 'graph [ dpi = 150 ];\n' #ESE 50 ES EL TAMAÑO DE LA IMAGEN 
    codigo += 'a0 [shape=none label=<\n'
    codigo += '<TABLE border="0" cellspacing="5" cellpadding="4" style="rounded" bgcolor="/rdylgn11/11:/rdylgn11/1">\n'
    codigo += '<TR>\n'
    codigo += '<TD colspan="1" bgcolor="#EFC8B2"><FONT POINT-SIZE="14"><B>NUMERO</B></FONT></TD>\n' 
    codigo += '<TD colspan="1" bgcolor="#EFC8B2"><FONT POINT-SIZE="14"><B>TIPO</B></FONT></TD>\n'
    codigo += '<TD colspan="1" bgcolor="#EFC8B2"><FONT POINT-SIZE="14"><B>DESCRIPCION</B></FONT></TD>\n'
    codigo += '<TD colspan="1" bgcolor="#EFC8B2"><FONT POINT-SIZE="14"><B>LINEA</B></FONT></TD>\n'
    codigo += '</TR>\n'
    
    for i in range(len(lista_errores)):
        error = lista_errores[i]
        if(isinstance(error,ERROR_LSS)):
            #print(error.descripcion)
            codigo += '<TR>\n'
            codigo += '<TD  colspan="1" bgcolor="#ffffd4"><FONT POINT-SIZE="12">'+str(i+1)+'</FONT></TD>\n'
            codigo += '<TD  colspan="1" bgcolor="#ffffd4"><FONT POINT-SIZE="12">'+str(error.tipo)+'</FONT></TD>\n'
            codigo += '<TD  colspan="1" bgcolor="#ffffd4"><FONT POINT-SIZE="12">'+str(error.descripcion)+'</FONT></TD>\n'
            codigo += '<TD  colspan="1" bgcolor="#ffffd4"><FONT POINT-SIZE="12">'+str(error.linea)+'</FONT></TD>\n'
            codigo += '</TR>\n'

    codigo += '</TABLE>>];\n'
    codigo += '}\n'
    return(codigo)



