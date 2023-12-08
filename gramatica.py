from FUNCIONES.ARBOL.VALOR import *
from FUNCIONES.DDL.CREATE_BASE import *
from FUNCIONES.FUNCIONES_SISTEMA.CONCATENAR import *
tokens = (
    'SELECT', 'FROM', 'WHERE', 'AS', 'CREATE', 'TABLE', 'DATA', 'BASE', 
    'CONCATENAR', 'SUBSTRAER', 'HOY', 'CONTAR', 'SUMA',
    'CAST', 'MAS', 'RESTA', 'MULTIPLICACION', 'DIVISION', 
    'IGUAL', 'IGUALIGUAL', 'DIFERENTE', 'MAYORQUE', 'MENORQUE', 'MAYORIGUAL', 'MENORIGUAL', 
    'OR', 'AND', 'RNOT',
    'PARABRE', 'PARCIERRA', 'COMA', 'ARROBA', 'PTCOMA',
    'NINT', 'NBIT', 'NDECIMAL', 'FECHA', 'FECHAHORA', 'CADENA', 
    'NOMBRE', 'INT', 'BIT', 'DECIMAL', 'DATE', 'DATETIME', 'NCHAR', 'NVARCHAR',
    'NOT', 'NULL', 'PRIMARY', 'KEY', 'FOREIGN', 'REFERENCE', 
    'INSERT', 'INTO', 'VALUES', 'DELETE'
)

#Tokens
t_INT               =   r'(?i)INT'
t_BIT               =   r'(?i)BIT'
t_DECIMAL           =   r'(?i)DECIMAL'
t_DATE              =   r'(?i)DATE'
t_DATETIME          =   r'(?i)DATETIME'
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



def t_FECHA(t):
    r'\d\d\-\d\d\-\d\d\d\d'
    try:
        t.value = t.value
    except ValueError:
        print("VALOR FECHA INCORRECTO %d",t.value)
    return t.value

def t_FECHAHORA(t):
    r'\d\d\-\d\d\-\d\d\d\d\-\d\d\:\d\d'
    try:
        t.value = t.value
    except ValueError:
        print("VALOR FECHA HORA INCORRECTO %d",t.value)
    return t.value

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

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
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

#DEFINICION DE LA GRAMATICA
def p_instrucciones_lista(t):
    '''instrucciones   : instruccion instrucciones 
                       | instruccion '''
    listado_instrucciones.append(t[1])  #GUARDA CADA INSTRUCCION (DEBEN SER OBJETOS)
    t[0] = listado_instrucciones        #PARA DEVOLVER LA LISTA ACTUALIZADA
    
def p_instrucciones_evaluar(t):
    '''instruccion  : f_sistema
                    | exp_aritmetica 
                    | exp_relacional
                    | exp_logica
                    | sent_create_database
                    | sent_create_table
                    | f_insert 
                    | f_delete
                    '''
    t[0] = t[1]


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
    #print("CONCATENAR -> "+str(t[3] +" , "+str(t[5])))
    t[0] = CONCATENAR(t[3],t[5],lexer.lineno,0)
    

def p_substraer(t):
    'func_substraer : SUBSTRAER PARABRE CADENA COMA NINT COMA NINT PARCIERRA'
    print("SUBSTRAER -> "+str(t[3]) +" , "+ str(t[5])+" , "+str(t[7]))

def p_hoy(t):
    'func_hoy : HOY PARABRE PARCIERRA'
    print("HOY -> HOY")

def p_contar(t):
    'func_contar : CONTAR PARABRE MULTIPLICACION PARCIERRA FROM name WHERE name IGUAL expresion'
    print("CONTAR -> "+str(t[6]) + " , "+ str(t[8] + " , " + str(t[10])))

def p_suma(t):
    'func_suma : SUMA PARABRE name PARCIERRA FROM name WHERE name IGUAL expresion'
    print("SUMA -> " + str(t[3]) + " , "+str(t[6]) + " , "+ str(t[8]) + " , " + str(t[10]))

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
    
def p_adicion(t):
    '''op_suma : numero MAS numero '''
    print("SUMA ENTRE: "+str(t[1]) + " y "+ str(t[3]))

def p_resta(t):
    '''op_resta : numero RESTA numero '''
    print("RESTA ENTRE: "+str(t[1]) + " y "+ str(t[3]))

def p_multiplicacion(t):
    '''op_multiplicacion : numero MULTIPLICACION numero '''
    print("MULTIPLICACION ENTRE: "+str(t[1]) + " y "+ str(t[3]))

def p_division(t):
    '''op_division : numero DIVISION numero '''
    print("DIVISION ENTRE: "+str(t[1]) + " y "+ str(t[3]))



def p_expresion_relacional(t):
    '''exp_relacional   : exr_igual
                        | exr_diferente
                        | exr_menorque
                        | exr_mayorque
                        | exr_menorigual
                        | exr_mayorigual'''

def p_igual(t):
    '''exr_igual : expresion IGUALIGUAL expresion'''
    print("RELACIONAL IGUAL -> "+str(t[1]) +" , "+str(t[3]))

def p_diferente(t):
    '''exr_diferente : expresion DIFERENTE expresion'''
    print("RELACIONAL DIFERENTE -> "+str(t[1]) +" , "+str(t[3]))

def p_menorque(t):
    '''exr_menorque : expresion MENORQUE expresion'''
    print("RELACIONAL MENOR QUE -> "+str(t[1]) +" , "+str(t[3]))

def p_mayorque(t):
    '''exr_mayorque : expresion MAYORQUE expresion'''
    print("RELACIONAL MAYOR QUE -> "+str(t[1]) +" , "+str(t[3]))

def p_menorigual(t):
    '''exr_menorigual : expresion MENORIGUAL expresion'''
    print("RELACIONAL MENOR O IGUAL QUE -> "+str(t[1]) +" , "+str(t[3]))

def p_mayorigual(t):
    '''exr_mayorigual : expresion MAYORIGUAL expresion'''
    print("RELACIONAL MAYOR O IGUAL QUE -> "+str(t[1]) +" , "+str(t[3]))



def p_expresion_logica(t):
    '''exp_logica : exl_and'''

def p_and(t):
    '''exl_and : expresion AND expresion'''
    print("LOGICA AND -> "+str(t[1])+" , "+str(t[3]))

def p_or(t):
    '''exl_and : expresion OR expresion'''
    print("LOGICA OR -> "+str(t[1])+" , "+str(t[3]))

def p_not(t):
    '''exl_and : RNOT expresion %prec RNOT'''
    print("LOGICA NOT -> "+str(t[2]))



def p_sentencia_create_database(t):
    '''sent_create_database : CREATE DATA BASE name PTCOMA '''
    t[0] = CREATE_BASE(t[4],lexer.lineno,0)


def p_sentencia_create_table(t):
    '''sent_create_table : CREATE TABLE name PARABRE datos PARCIERRA PTCOMA'''
    print("SE VA A CREAR UNA TABLE")

def p_datos(t):
    '''datos : name tipo_dato
             | name tipo_dato caracteristicas
             | foreign_key
             | datos COMA datos '''
    try:
        if(t[1]!=None):
            print(t[1])
    except:
        print("")     
    
def p_foreign_key(t):
    '''foreign_key : FOREIGN KEY PARABRE name PARCIERRA REFERENCE name PARABRE name PARCIERRA'''
    print("HAY UN FOREIGN KEY")

def p_caracteristicas(t):
    '''caracteristicas : NULL
                        | NOT NULL
                        | PRIMARY KEY
                        | NOT NULL PRIMARY KEY
                        | NULL PRIMARY KEY
                        '''

def p_f_insert(t):
    ''' f_insert :  INSERT INTO name PARABRE columnas PARCIERRA VALUES PARABRE valores PARCIERRA PTCOMA'''
    print("INSERTAR -> " +str(t[3]) )
    

def p_f_delete(t):
    ''' f_delete : DELETE FROM name WHERE name IGUAL expresion PTCOMA'''
    print("DELETE -> "+str(t[3]))

def p_columnas(t):
    ''' columnas : name
                | name COMA columnas'''
def p_valores(t):
    ''' valores : expresion
                | expresion COMA valores'''

def p_tipodato(t):
    '''tipo_dato : INT 
                 | BIT
                 | DECIMAL
                 | DATE
                 | DATETIME
                 | dato_nchar
                 | dato_nvarchar'''
    t[0] = t[1]
    
def p_dato_nchar(t):
    '''dato_nchar : NCHAR PARABRE NINT PARCIERRA'''

def p_dato_nvarchar(t):
    '''dato_nvarchar : NVARCHAR PARABRE NINT PARCIERRA'''
    

def p_expresion(t):
    '''expresion : numero
                 | FECHA
                 | FECHAHORA
                 | CADENA'''
    
    if(t.slice[1].type == "FECHA"):
        t[0] = VALOR(t[1],"FECHA",lexer.lineno,0)
    elif(t.slice[1].type == "FECHAHORA"):
        t[0] = VALOR(t[1],"FECHAHORA",lexer.lineno,0)
    elif(t.slice[1].type == "CADENA"):
        t[0] = VALOR(t[1],"CADENA",lexer.lineno,0)
    else:
        t[0] = t[1]
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

def p_error(t):
    print("Error sintáctico en '%s'" % t.value)





import ply.yacc as yacc
parser = yacc.yacc()

#pruebas
#f = open("./entrada.txt", "r")      #ABRIR ARCHIVO
#input = f.read()                    #LEER CONTENIDO
#print(input)                        #MOSTRAR EL CONTENIDO
#parser.parse(input)                 #ANALIZARLO