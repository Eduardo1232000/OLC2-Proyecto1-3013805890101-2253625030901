SELECT * FROM nombre_tabla;
SELECT * FROM name PTCOMA

SELECT columna1, columna2 FROM nombre_tabla;
SELECT columnas FROM name PTCOMA


SELECT * FROM nombre_tabla WHERE condicion;
SELECT * FROM name condiciones_opt PTCOMA

SELECT columna1, columna 2 FROM nombre_tabla WHERE condicion1 AND condicion2;
SELECT columnas FROM name condiciones_opt PTCOMA

def p_f_select(t):
    ''' f_select : SELECT select_columnas FROM name condiciones_opt PTCOMA'''
    #t[0] = SELECT(t[3], t[4], t[5], lexer.lineno, 0)
    print("funciona" +str(t[3]) + " " +str(t[4]))

def p_select_columnas(t):
    ''' select_columnas : MULTIPLICACION
                        | columnas
                        | FROM name'''
    if t.slice[1].type == 'MULTIPLICACION':
        #t[0] = SELECT_ALL_COLUMNS()
        print( 'algo')
    elif t.slice[1].type == 'FROM':
        t[0] = None
    else:
        t[0] = t[1]