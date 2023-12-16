from FUNCIONES.ARBOL.NODO_TABLA_SIMBOLOS import *

def obtener_codigo_grafica_reporte_tabla_simbolos(lista_tabla_simbolos):
    codigo = "digraph G{\n"
    codigo += 'graph [ dpi = 150 ];\n' #ESE 50 ES EL TAMAÑO DE LA IMAGEN 
    codigo += 'a0 [shape=none label=<\n'
    codigo += '<TABLE border="0" cellspacing="5" cellpadding="4" style="rounded" bgcolor="/rdylgn11/5:/rdylgn11/7">\n'
    codigo += '<TR>\n'
    codigo += '<TD colspan="1" bgcolor="#DEC682"><FONT POINT-SIZE="14"><B>NUMERO</B></FONT></TD>\n' 
    codigo += '<TD colspan="1" bgcolor="#DEC682"><FONT POINT-SIZE="14"><B>IDENTIFICADOR</B></FONT></TD>\n'
    codigo += '<TD colspan="1" bgcolor="#DEC682"><FONT POINT-SIZE="14"><B>TIPO<br/>RETORNO</B></FONT></TD>\n'
    codigo += '<TD colspan="1" bgcolor="#DEC682"><FONT POINT-SIZE="14"><B>BASE<br/>ENCONTRADA</B></FONT></TD>\n'
    codigo += '<TD colspan="1" bgcolor="#DEC682"><FONT POINT-SIZE="14"><B>TIPO</B></FONT></TD>\n'
    codigo += '<TD colspan="1" bgcolor="#DEC682"><FONT POINT-SIZE="14"><B>DIMENSION</B></FONT></TD>\n'
    codigo += '<TD colspan="1" bgcolor="#DEC682"><FONT POINT-SIZE="14"><B>DECLARADA EN <br/>(AMBITO)</B></FONT></TD>\n'
    codigo += '<TD colspan="1" bgcolor="#DEC682"><FONT POINT-SIZE="14"><B>REFERENCIA</B></FONT></TD>\n'
    codigo += '</TR>\n'
    
    for i in range(len(lista_tabla_simbolos)):
        error = lista_tabla_simbolos[i]
        if(isinstance(error,NODO_TABLA_SIMBOLOS)):
            #print(error.descripcion)
            codigo += '<TR>\n'
            codigo += '<TD  colspan="1" bgcolor="#ffffd4"><FONT POINT-SIZE="12">'+str(i+1)+'</FONT></TD>\n'
            codigo += '<TD  colspan="1" bgcolor="#ffffd4"><FONT POINT-SIZE="12">'+str(error.identificador)+'</FONT></TD>\n'
            codigo += '<TD  colspan="1" bgcolor="#ffffd4"><FONT POINT-SIZE="12">'+str(error.obtener_tipo_var_fun())+'</FONT></TD>\n'
            codigo += '<TD  colspan="1" bgcolor="#ffffd4"><FONT POINT-SIZE="12">'+str(error.obtener_base())+'</FONT></TD>\n'
            codigo += '<TD  colspan="1" bgcolor="#ffffd4"><FONT POINT-SIZE="12">'+str(error.obtener_tipo())+'</FONT></TD>\n'
            codigo += '<TD  colspan="1" bgcolor="#ffffd4"><FONT POINT-SIZE="12">'+str(error.obtener_dimension())+'</FONT></TD>\n'
            codigo += '<TD  colspan="1" bgcolor="#ffffd4"><FONT POINT-SIZE="12">'+str(error.obtener_entorno())+'</FONT></TD>\n'
            codigo += '<TD  colspan="1" bgcolor="#ffffd4"><FONT POINT-SIZE="12">'+str(error.obtener_referencia())+'</FONT></TD>\n'
            codigo += '</TR>\n'

    codigo += '</TABLE>>];\n'
    codigo += '}\n'
    return(codigo)



