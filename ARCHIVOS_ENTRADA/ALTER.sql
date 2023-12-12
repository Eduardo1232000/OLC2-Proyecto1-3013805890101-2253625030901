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

ALTER TABLE table_name ADD COLUMN column_name tipo_dato;
ALTER TABLE table_name ADD CONSTRAINT constraint_name FOREIGN KEY (column_name) REFERENCES reference_table(reference_column);
ALTER TABLE table_name DROP COLUMN column_name;
ALTER TABLE table_name DROP CONSTRAINT constraint_name;
ALTER TABLE table_name MODIFY COLUMN column_name tipo_dato;
