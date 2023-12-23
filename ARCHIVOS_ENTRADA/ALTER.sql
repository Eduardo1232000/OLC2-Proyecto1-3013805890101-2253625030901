ALTER TABLE NOMBRETABLA ADD
NOMBRECOLUMNA TIPO
ALTER TABLE NOMBRETABLA
DROP NOMBRECOLUMNA



ALTER TABLE table_name ADD COLUMN column_name INT;
ALTER TABLE table_name ADD CONSTRAINT constraint_name FOREIGN KEY (column_name) REFERENCES reference_table(reference_column);
ALTER TABLE table_name DROP COLUMN column_name;
ALTER TABLE table_name DROP CONSTRAINT constraint_name;
ALTER TABLE table_name MODIFY COLUMN column_name tipo_dato;
