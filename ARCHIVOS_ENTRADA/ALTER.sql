ALTER TABLE NOMBRETABLA ADD
NOMBRECOLUMNA TIPO
ALTER TABLE NOMBRETABLA
DROP NOMBRECOLUMNA


def p_f_insert(t):
    ''' f_insert :  INSERT INTO name PARABRE columnas PARCIERRA VALUES PARABRE valores PARCIERRA PTCOMA'''
    t[0] = INSERT_INTO(t[3],t[5],t[9],lexer.lineno,0)

    USE Alimentos;

INSERT INTO products (product_no, name, id_producto)
VALUES (1,"Manzana",1);

USE Perro;
ALTER TABLE raza ADD COLUMN age INT;
ALTER TABLE raza DROP COLUMN age;
ALTER TABLE table_name ADD COLUMN column_name INT;
ALTER TABLE table_name ADD CONSTRAINT constraint_name FOREIGN KEY (column_name) REFERENCES reference_table(reference_column);
ALTER TABLE table_name DROP COLUMN column_name;
ALTER TABLE table_name DROP CONSTRAINT constraint_name;
ALTER TABLE table_name MODIFY COLUMN column_name tipo_dato;



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
        t[0] = ("ADD", t[3], t[4])
    elif len(t) == 14:
        t[0] = ("ADD_CONSTRAINT", t[3], t[5], t[10], t[12], t[13])
    else:
        # Manejar un error si la estructura no coincide
        t[0] = None

def p_alter_drop(t):
    '''alter_drop : DROP COLUMN name
                  | DROP CONSTRAINT name'''
    if len(t) == 4:
        t[0] = ("DROP", t[3])
    elif len(t) == 3:
        t[0] = ("DROP_CONSTRAINT", t[3])
    else:
        # Manejar un error si la estructura no coincide
        t[0] = None

def p_alter_modify(t):
    '''alter_modify : MODIFY COLUMN name tipo_dato'''
    t[0] = ("MODIFY", t[4])