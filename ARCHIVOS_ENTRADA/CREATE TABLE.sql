USE Alimentos;

CREATE TABLE products (
 product_no int PRIMARY KEY ,
 name char(5) NULL ,
 id_producto int NOT NULL,
FOREIGN KEY (name) REFERENCE 
Identificaciones(nombre)
);



