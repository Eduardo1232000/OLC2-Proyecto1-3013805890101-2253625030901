from FUNCIONES.ARBOL.VALOR import *
from FUNCIONES.ARBOL.TIPO import *
from FUNCIONES.DDL.CREATE_BASE import *
from FUNCIONES.DDL.USE_BASE import *
from FUNCIONES.DDL.CREATE_TABLE import * 
from FUNCIONES.DDL.DECLARE import *

from FUNCIONES.DDL.ALTER_TABLE import *
from FUNCIONES.DDL.DROP import*

from FUNCIONES.DDL.INSERT_INTO import *


from FUNCIONES.FUNCIONES_SISTEMA.CONCATENAR import *
from FUNCIONES.FUNCIONES_SISTEMA.SUBSTRAER import *
from FUNCIONES.FUNCIONES_SISTEMA.HOY import *
from FUNCIONES.FUNCIONES_SISTEMA.CONTAR import *
from FUNCIONES.FUNCIONES_SISTEMA.SELECT_SUMA import *

from FUNCIONES.OPERACIONES_ARITMETICAS.SUMA import *
from FUNCIONES.OPERACIONES_ARITMETICAS.RESTA import *
from FUNCIONES.OPERACIONES_ARITMETICAS.MULTIPLICACION import *
from FUNCIONES.OPERACIONES_ARITMETICAS.DIVISION import *

from FUNCIONES.OPERACIONES_RELACIONAL.IGUAL import *
from FUNCIONES.OPERACIONES_RELACIONAL.DIFERENTE import *
from FUNCIONES.OPERACIONES_RELACIONAL.MENOR_QUE import *
from FUNCIONES.OPERACIONES_RELACIONAL.MAYOR_QUE import *
from FUNCIONES.OPERACIONES_RELACIONAL.MENOR_IGUAL import *
from FUNCIONES.OPERACIONES_RELACIONAL.MAYOR_IGUAL import *

from FUNCIONES.OPERACIONES_LOGICAS.AND import *
from FUNCIONES.OPERACIONES_LOGICAS.OR import *
from FUNCIONES.OPERACIONES_LOGICAS.NOT import *

from FUNCIONES.ERROR_LSS import *


tokens = (
    'SELECT', 'FROM','USE', 'WHERE', 'AS', 'CREATE', 'TABLE', 'DATA', 'BASE', 
    'CONCATENAR', 'SUBSTRAER', 'HOY', 'CONTAR', 'SUMA',
    'CAST', 'MAS', 'RESTA', 'MULTIPLICACION', 'DIVISION', 
    'IGUAL', 'IGUALIGUAL', 'DIFERENTE', 'MAYORQUE', 'MENORQUE', 'MAYORIGUAL', 'MENORIGUAL', 
    'OR', 'AND', 'RNOT',
    'PARABRE', 'PARCIERRA', 'COMA', 'ARROBA', 'PTCOMA',
    'NINT', 'NBIT', 'NDECIMAL', 'FECHA', 'FECHAHORA', 'CADENA', 
    'NOMBRE', 'INT', 'BIT', 'DECIMAL','DATETIME', 'DATE',  'NCHAR', 'NVARCHAR',
    'NOT', 'NULL', 'PRIMARY', 'KEY', 'FOREIGN', 'REFERENCE', 
    'INSERT', 'INTO', 'VALUES', 'DELETE',
    'ALTER', 'DROP', 'TRUNCATE',
    'ADD', 'MODIFY',
    'COLUMN', 'CONSTRAINT', 'REFERENCES','DECLARE', 'SET'
)

#Tokens
t_INT               =   r'(?i)INT'
t_BIT               =   r'(?i)BIT'
t_DECIMAL           =   r'(?i)DECIMAL'
t_DATETIME          =   r'(?i)DATETIME'
t_DATE              =   r'(?i)DATE'
t_NCHAR             =   r'(?i)NCHAR'
t_NVARCHAR          =   r'(?i)NVARCHAR'
t_NOT               =   r'(?i)NOT'
t_NULL              =   r'(?i)NULL'
t_PRIMARY           =   r'(?i)PRIMARY'
t_FOREIGN           =   r'(?i)FOREIGN'
t_REFERENCE         =   r'(?i)REFERENCE'
t_KEY               =   r'(?i)KEY'
t_SELECT            =   r'(?i)SELECT' 
t_FROM              =   r'(?i)FROM'
t_USE               =   r'(?i)USE'
t_WHERE             =   r'(?i)WHERE'
t_CAST              =   r'(?i)CAST'
t_AS                =   r'(?i)AS'
t_CREATE            =   r'(?i)CREATE'
t_TABLE             =   r'(?i)TABLE'
t_DATA              =   r'(?i)DATA'
t_BASE              =   r'(?i)BASE'
t_CONCATENAR        =   r'(?i)CONCATENAR'
t_SUBSTRAER         =   r'(?i)SUBSTRAER'
t_HOY               =   r'(?i)HOY'
t_CONTAR            =   r'(?i)CONTAR'
t_SUMA              =   r'(?i)SUMA'
t_INSERT            =   r'(?i)INSERT'
t_INTO              =   r'(?i)INTO'
t_VALUES            =   r'(?i)VALUES'
t_DELETE            =   r'(?i)DELETE'
t_DECLARE           =   r'(?i)DECLARE'
t_SET               =   r'(?i)SET'

t_MAS               =   r'\+'
t_RESTA             =   r'-'
t_MULTIPLICACION    =   r'\*'
t_DIVISION          =   r'/'
t_IGUAL             =   r'='
t_IGUALIGUAL        =   r'=='
t_DIFERENTE         =   r'!='
t_MAYORQUE          =   r'>'
t_MENORQUE          =   r'<'
t_MAYORIGUAL        =   r'>='
t_MENORIGUAL        =   r'<='
t_OR                =   r'\|\|'
t_AND               =   r'\&\&'
t_RNOT               =   r'\!'
t_PARABRE           =   r'\('
t_PARCIERRA         =   r'\)'
t_COMA              =   r'\,'
t_ARROBA            =   r'\@'
t_PTCOMA            =   r'\;'


def t_FECHAHORA(t):
    r'\d{2}-\d{2}-\d{4}\s\d{2}:\d{2}'
    try:
        t.value = t.value
    except ValueError:
        print("VALOR FECHA HORA INCORRECTO %s", t.value)
    return t

def t_FECHA(t):
    #r'\d\d\-\d\d\-\d\d\d\d'
    r'\d{2}-\d{2}-\d{4}'
    try:
        t.value = str(t.value)
    except ValueError:
        print("VALOR FECHA INCORRECTO %d",t.value)
    return t


def t_NDECIMAL(t):
    r'-?\d+\.\d+'
    try:
        print("RECONOCI DECIMAL: " +str(t.value))
        t.value = float(t.value)
    except ValueError:
        print("VALOR FLOAT DEMASIADO LARGO %d",t.value)
        t.value = 0.0
    return t

def t_NINT(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("VALOR ENTERO DEMASIADO LARGO %d", t.value)
        t.value = 0
    return t

def t_NBIT(t):
    r'0|1'
    try:
        t.value = int(t.value)
    except ValueError:
        print("VALOR BIT DEMASIADO LARGO %d",t.value)
        t.value = 0
    return t






def t_CADENA(t):
    r'\"([^"]*)\"'
    try:
        t.value = str(t.value[1:-1])
    except ValueError:
        print("VALOR CADENA INCORRECTO %s" % t.value)
        t.value = ""
    return t

def t_NOMBRE(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    try:
        if t.value.upper() in [x.upper() for x in tokens]:
            t.type = t.value.upper()
        else:
            t.value = str(t.value)  
    except ValueError:
        print("VALOR CADENA INCORRECTO %s" % t.value)
        t.value = ""
    return t

#CARACTERES IGNORADOS
t_ignore = " \t"


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_NULLL(t):
    r'NULL'
    pass  # No hace nada, simplemente ignora el token 'NULL'

def t_error(t):
    #print("Illegal character '%s'" % t.value[0])
    er = ERROR_LSS("LEXICO",str(t.value[0])+" No pertenece al lenguaje",lexer.lineno)
    lista_error_lexico.append(er)
    
    t.lexer.skip(1)
    

#CONSTRUYENDO EL ANALIZADOR LEXICO
import ply.lex as lex
lexer = lex.lex()


#ASOCIACION DE OPERADORES Y PRECEDENCIA
precedence = (
    ('left','SUMA', 'RESTA'),
    ('left','MULTIPLICACION','DIVISION'),
    ('left','IGUALIGUAL','DIFERENTE','MAYORQUE','MENORQUE','MAYORIGUAL','MENORIGUAL'),
    ('left','OR'),
    ('left','AND'),
    ('left','PARABRE','PARCIERRA'),
    ('right','RNOT')
)


listado_instrucciones = []      #LISTA GLOBAL
lista_error_sintactico = []      
lista_error_lexico = []


#DEFINICION DE LA GRAMATICA
def p_instrucciones_lista(t):
    '''instrucciones   : instruccion instrucciones 
                       | instruccion '''

    if len(t) == 2:
        t[0] = [[t[1]], lista_error_lexico, lista_error_sintactico]
    else:

        t[2][0].insert(0, t[1])
        t[0] = t[2]
        #AGREGAR LOS ERRORES LEXICOS Y SINTACTICOS

    
def p_instrucciones_evaluar(t):
    '''instruccion  : f_sistema
                    | exp_logica
                    | sent_create_database
                    | sent_create_table
                    | use_base
                    | f_insert 
                    | f_delete
                    | expresion 
                    | sent_alter_table
                    | sent_drop
                    | sent_truncate
                    | declarar_var
                    | asignacion_variable
                    '''
    #EXPRESION ES TEMPORAL (SOLO PARA VER SU FUNCIONAMIENTO)
    t[0] = t[1]
def p_declaracion_variable(t):
    ''' declarar_var : DECLARE ARROBA name tipo_dato PTCOMA'''
    t[0] = DECLARE(t[3],t[4],lexer.lineno,0)

def p_asignacion_variable(t):
    ''' asignacion_variable : SET ARROBA name IGUAL expresion PTCOMA'''
    t[0] = ASIGNAR_VARIABLE(t[3],t[5],lexer.lineno,0)

def p_funcion_sistema(t):
    ''' f_sistema : SELECT operacion_sis'''
    t[0] = t[2]

def p_operacion_sistema(t):
    '''operacion_sis : func_concatena
                    | func_substraer
                    | func_hoy
                    | func_contar
                    | func_suma
                    | func_cas
                    | select_dato
                    '''
    t[0] = t[1]



def p_concatena(t):
    'func_concatena : CONCATENAR PARABRE expresion COMA expresion PARCIERRA'
    t[0] = CONCATENAR(t[3],t[5],lexer.lineno,0)

def p_substraer(t):
    'func_substraer : SUBSTRAER PARABRE cadenas COMA numero COMA numero PARCIERRA'
    #print("SUBSTRAER -> "+str(t[3]) +" , "+ str(t[5])+" , "+str(t[7]))
    t[0] = SUBSTRAER(t[3],t[5],t[7],lexer.lineno,0)

def p_hoy(t):
    'func_hoy : HOY PARABRE PARCIERRA'
    t[0] = HOY(lexer.lineno,0)

def p_contar(t):
    '''func_contar : CONTAR PARABRE MULTIPLICACION PARCIERRA FROM name WHERE name IGUAL expresion PTCOMA
                   | CONTAR PARABRE MULTIPLICACION PARCIERRA FROM name WHERE name signo_relacional expresion PTCOMA'''
    
    t[0] = CONTAR(t[3],t[6],t[8],t[9],t[10],lexer.lineno,0)

def p_signo_relacional(t):
    '''signo_relacional : DIFERENTE
                        | MENORQUE
                        | MAYORQUE
                        | MENORIGUAL
                        | MAYORIGUAL'''
    t[0] = t[1]
def p_suma(t):
    '''func_suma : SUMA PARABRE name PARCIERRA FROM name WHERE name IGUAL expresion PTCOMA
                 | SUMA PARABRE name PARCIERRA FROM name WHERE name signo_relacional expresion PTCOMA'''
    t[0] = SELECT_SUMA(t[3],t[6],t[8],t[9],t[10],lexer.lineno,0)

def p_cas(t):
    'func_cas : CAST PARABRE ARROBA name AS tipo_dato PARCIERRA '
    print("CAST -> "+str(t[4]) + " -> " +str(t[6]))

def p_select_dato(t):
    '''select_dato : MULTIPLICACION FROM name
                    | FROM name
                    | FROM name WHERE condiciones'''
    print("SELECCIONANDO TODOS LOS DATOS DE: " +str(t[3]))

def p_condiciones (t):
    '''condiciones : expresion
                    | expresion AND condiciones
                    | expresion OR condiciones '''

def p_expresion_aritmetica(t):
    '''exp_aritmetica   : op_suma
                        | op_resta
                        | op_multiplicacion
                        | op_division'''
    t[0] = t[1]
    
def p_adicion(t):
    '''op_suma : expresion MAS expresion '''
    t[0] = SUMA(t[1],t[3],lexer.lineno,0)

def p_resta(t):
    '''op_resta : expresion RESTA expresion '''
    t[0] = RESTA(t[1],t[3],lexer.lineno,0)

def p_multiplicacion(t):
    '''op_multiplicacion : expresion MULTIPLICACION expresion '''
    t[0] = MULTIPLICACION(t[1],t[3],lexer.lineno,0)

def p_division(t):
    '''op_division : expresion DIVISION expresion '''
    t[0] = DIVISION(t[1],t[3],lexer.lineno,0)



def p_expresion_relacional(t):
    '''exp_relacional   : exr_igual
                        | exr_diferente
                        | exr_menorque
                        | exr_mayorque
                        | exr_menorigual
                        | exr_mayorigual'''
    t[0] = t[1]

def p_igual(t):
    '''exr_igual : expresion IGUALIGUAL expresion'''
    t[0] = IGUAL(t[1],t[3],lexer.lineno,0)

def p_diferente(t):
    '''exr_diferente : expresion DIFERENTE expresion'''
    t[0] = DIFERENTE(t[1],t[3],lexer.lineno,0)

def p_menorque(t):
    '''exr_menorque : expresion MENORQUE expresion'''
    t[0] = MENOR_QUE(t[1],t[3],lexer.lineno,0)

def p_mayorque(t):
    '''exr_mayorque : expresion MAYORQUE expresion'''
    t[0] = MAYOR_QUE(t[1],t[3],lexer.lineno,0)

def p_menorigual(t):
    '''exr_menorigual : expresion MENORIGUAL expresion'''
    t[0] = MENOR_IGUAL(t[1],t[3],lexer.lineno,0)

def p_mayorigual(t):
    '''exr_mayorigual : expresion MAYORIGUAL expresion'''
    t[0] = MAYOR_IGUAL(t[1],t[3],lexer.lineno,0)



def p_expresion_logica(t):
    '''exp_logica : exl_and'''
    t[0] = t[1]

def p_and(t):
    '''exl_and : expresion AND expresion'''
    t[0] = EXP_AND(t[1],t[3],lexer.lineno,0)

def p_or(t):
    '''exl_and : expresion OR expresion'''
    t[0] = EXP_OR(t[1],t[3],lexer.lineno,0)

def p_not(t):
    '''exl_and : RNOT expresion %prec RNOT'''
    t[0] = EXP_NOT(t[2],lexer.lineno,0)



def p_sentencia_create_database(t):
    '''sent_create_database : CREATE DATA BASE name PTCOMA '''
    t[0] = CREATE_BASE(t[4],lexer.lineno,0)


def p_sentencia_create_table(t):
    '''sent_create_table : CREATE TABLE name PARABRE datos PARCIERRA PTCOMA'''
    t[0] = CREATE_TABLE(t[3],t[5],lexer.lineno,0)


#ALTER TABLE nombre_tabla ADD COLUMN new column TIPO DATO
#ALTER TABLE nombre_tabla DROP COLUMN nombre_columna
#ALTER TABLE nombre_tabla 'MODIFY' COLUMN nombre_columna name


def p_alter_table(t):
    '''sent_alter_table : ALTER TABLE name alter_action PTCOMA'''
    t[0] = ALTER_TABLE(t[3], t[4], lexer.lineno, 0)

def p_alter_action(t):
    '''alter_action : alter_add
                    | alter_drop
                    | alter_modify'''
    t[0] = t[1]

def p_alter_add(t):
    '''alter_add : ADD COLUMN name tipo_dato
                 | ADD CONSTRAINT name FOREIGN KEY PARABRE name PARCIERRA REFERENCES name PARABRE name PARCIERRA'''
    if len(t) == 5:
        t[0] = ("ADD", "COLUMN", t[3], t[4])
        print(f"tipo de dato en p_alter_add: {t[4]}")
    elif len(t) == 14:
        t[0] = ("ADD_CONSTRAINT", t[3], "FOREIGN KEY", t[5], "REFERENCES", t[10], t[12], t[13])
    else:
        # Manejar un error si la estructura no coincide
        t[0] = None

def p_alter_drop(t):
    '''alter_drop : DROP COLUMN name
                  | DROP CONSTRAINT name'''
    if len(t) == 4:
        t[0] = ("DROP", "COLUMN", t[3])
    elif len(t) == 3:
        t[0] = ("DROP_CONSTRAINT", t[3])
    else:
        # Manejar un error si la estructura no coincide
        t[0] = None

def p_alter_modify(t):
    '''alter_modify : MODIFY COLUMN name tipo_dato'''
    t[0] = ("MODIFY", "COLUMN", t[4], t[5])

#DROP TABLE nombre_tabla
#DROP DATABASE nombre_database

def p_sent_drop(t):
    '''sent_drop : DROP drop_type name PTCOMA'''
    t[0] = DROP(t[2], t[3], lexer.lineno,0)
    #print("DROP -> ")

def p_drop_type(t):
    '''drop_type : TABLE
                | DATA BASE'''
    t[0] = t[1]  # Usar t[1] (TABLE) o t[2] (DATA BASE) según la gramática
    #print("DROP TYPE -> " + str(t[0]))

#TRUNCATE TABLE nombre_tabla
def p_sent_truncate(t):
    '''sent_truncate : TRUNCATE TABLE name PTCOMA'''
    t[0] = TRUNCATE_TABLE(t[3], lexer.lineno, 0)
    print("Estoy recibiendo la gramatica correcta?")



def p_datos(t):
    '''datos : dato COMA datos
             | dato '''

    if len(t) == 2:
        # Solo hay una expresión
        t[0] = [t[1]]
    else:
        # Hay más de una expresión
        t[3].insert(0, t[1])
        t[0] = t[3]


def p_dato(t):
    '''dato : dato_con_caract
            | dato_sin_caract
            | foreign_key'''
    t[0] = t[1]     #PUEDE SER UN OBJETO O UNA LISTA

def p_dato_sin_caract(t):
    '''dato_sin_caract : name tipo_dato '''
    #print("campo sin caracteristicas")
    lista_dato = []
    lista_vacia = []
    lista_dato.append(t[1])#NOMBRE
    lista_dato.append(t[2])#TIPO
    lista_dato.append(lista_vacia)#LISTA DE CARACTERISTICAS
    t[0] = lista_dato
    lista_dato = []

def p_dato_con_caract(t):
    '''dato_con_caract : name tipo_dato caracteristicas'''
    #print("campo con caracteristicas")
    lista_dato = []
    lista_dato.append(t[1])#NOMBRE
    lista_dato.append(t[2])#TIPO
    lista_dato.append(t[3])#LISTA DE CARACTERISTICAS
    t[0] = lista_dato
    lista_dato = []

def p_user_base(t):
    '''use_base : USE name PTCOMA'''
    t[0] = USE_BASE(t[2],lexer.lineno,0)
         
    
def p_foreign_key(t):
    '''foreign_key : FOREIGN KEY PARABRE name PARCIERRA REFERENCE name PARABRE name PARCIERRA'''
    #print("HAY UN FOREIGN KEY")
    t[0] = FORANEA(t[7],t[4],t[9],lexer.lineno,0)

def p_caracteristicas(t):
    '''caracteristicas : caracteristica caracteristicas
                       | caracteristica
                        '''
    if len(t) == 2:     #SI SOLO ES UNA CARACTERISTICA
        t[0] = [t[1]]
    else:               #SI ES MAS DE 1 CARACTERISTICA
        t[2].insert(0, t[1])
        t[0] = t[2]

def p_caracteristica(t):
    '''caracteristica :  caract_nulo
                        | caract_no_nulo
                        | caract_primary_key
                        '''
    t[0] = t[1]

def p_caract_nulo(t):
    '''caract_nulo : NULL'''
    t[0] = TIPODATO(TIPO.NULL)

def p_caract_no_nulo(t):
    '''caract_no_nulo : NOT NULL'''
    t[0] = TIPODATO(TIPO.NOT_NULL)

def p_caract_primary_key(t):
    '''caract_primary_key : PRIMARY KEY'''
    t[0] = TIPODATO(TIPO.PRIMARY_KEY)

    
    

def p_f_insert(t):
    ''' f_insert :  INSERT INTO name PARABRE columnas PARCIERRA VALUES PARABRE valores PARCIERRA PTCOMA'''
    t[0] = INSERT_INTO(t[3],t[5],t[9],lexer.lineno,0)

    

def p_f_delete(t):
    ''' f_delete : DELETE FROM name WHERE name IGUAL expresion PTCOMA'''
    print("DELETE -> "+str(t[3]))

def p_columnas(t):
    ''' columnas : name
                | name COMA columnas'''
    if len(t) == 2:
        # Solo hay una expresión
        t[0] = [t[1]]
    else:
        # Hay más de una expresión
        t[3].insert(0, t[1])
        t[0] = t[3]
                
    


def p_valores(t):
    ''' valores : expresion
                | expresion COMA valores'''
    
    if len(t) == 2:
        # Solo hay una expresión
        t[0] = [t[1]]
    else:
        # Hay más de una expresión
        t[3].insert(0, t[1])
        t[0] = t[3]

def p_tipodato(t):
    '''tipo_dato : INT 
                 | BIT
                 | DECIMAL
                 | DATE
                 | DATETIME
                 | dato_char
                 | dato_varchar'''
    if(t.slice[1].type == "INT"):
        t[0] = TIPODATO(TIPO.INT)
    elif(t.slice[1].type == "BIT"):
        t[0] = TIPODATO(TIPO.BIT)
    elif(t.slice[1].type == "DECIMAL"):
        t[0] = TIPODATO(TIPO.DECIMAL)
    elif(t.slice[1].type == "DATE"):
        t[0] = TIPODATO(TIPO.DATE)
    elif(t.slice[1].type == "DATETIME"):
        t[0] = TIPODATO(TIPO.DATETIME)
    else:
        t[0] = t[1]
    
def p_dato_char(t):
    '''dato_char : NCHAR PARABRE NINT PARCIERRA'''
    t[0] = TIPODATO(TIPO.NCHAR,t[3]) #PARA EL TIPODATO ES EL UNICO DONDE NO MANEJA OBJETO PARA EL NUMERO DEL CHAR O VARCHAR


def p_dato_varchar(t):
    '''dato_varchar : NVARCHAR PARABRE NINT PARCIERRA'''
    t[0] = TIPODATO(TIPO.NVARCHAR,t[3])
    

def p_expresion(t):
    '''expresion : exp_aritmetica
                 | exp_relacional
                 | variable
                 | parentesis
                 | numero
                 | FECHA
                 | FECHAHORA
                 | CADENA
                 '''
    
    if(t.slice[1].type == "FECHA"):
        t[0] = VALOR(t[1],"FECHA",lexer.lineno,0)
    elif(t.slice[1].type == "FECHAHORA"):
        t[0] = VALOR(t[1],"FECHAHORA",lexer.lineno,0)
    elif(t.slice[1].type == "CADENA"):
        t[0] = VALOR(t[1],"CADENA",lexer.lineno,0)
    else:
        t[0] = t[1]

def p_variable(t):
    '''variable : ARROBA name '''
    t[0] = VALIDAR_EXISTE_VARIABLE(t[2],lexer.lineno,0)



def p_parentesisop(t):
    '''parentesis : PARABRE expresion PARCIERRA'''
    t[0] = t[2]

def p_numero(t):
    '''numero : NINT
             | NBIT
             | NDECIMAL'''
    if(t.slice[1].type == "NINT"):
        t[0] = VALOR(t[1],"INT",lexer.lineno,0)
    elif(t.slice[1].type == "NBIT"):
        t[0] = VALOR(t[1],"BIT",lexer.lineno,0)
    elif(t.slice[1].type == "NDECIMAL"):
        t[0] = VALOR(t[1],"DECIMAL",lexer.lineno,0)
    else:
        t[0] = t[1]     #CASO DE ERROR

def p_name(t):
    '''name : NOMBRE'''     
    t[0] = VALOR(t[1],"CADENA",lexer.lineno,0)

def p_cadena(t):
    '''cadenas : CADENA'''     
    t[0] = VALOR(t[1],"CADENA",lexer.lineno,0)

def p_error(t):
    if t is not None:
        print("Error sintáctico en '%s'" % t.value)
        er = ERROR_LSS("SINTACTICO",str(t.value)+" Genera un error en la sintaxis",lexer.lineno)
        lista_error_sintactico.append(er)

        reiniciar_parser()
        while True:
            tok = lexer.token()
            if not tok or tok.type == 'PTCOMA'or tok.type == 'NULL':
                break
    else:
        print("Error: Vacio")

def reiniciar_parser():
    global parser
    parser = yacc.yacc()

def reiniciar_lexer():
    global lexer
    lexer = lex.lex()



import ply.yacc as yacc
parser = yacc.yacc()

def parses(data):
    global listado_instrucciones
    global lista_error_sintactico
    global lista_error_lexico
    listado_instrucciones = []  #EN CADA ANALISIS SE VACIA  
    lista_error_sintactico = []
    lista_error_lexico = []
 
    parser = yacc.yacc()
    
    result = parser.parse(data)
    return result

#input_text = input("ingrese la expresion: ")
#parser.parse(input_text)