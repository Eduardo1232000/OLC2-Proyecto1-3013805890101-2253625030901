USE Alimentos;

CREATE TABLE products (
 product_no int PRIMARY KEY ,
 name char(5) NULL ,
 id_producto int NOT NULL,
FOREIGN KEY (name) REFERENCE 
Identificaciones(nombre)
);



USE perrito;

CREATE TABLE raza (
 id int PRIMARY KEY ,
 name char(5) NULL ,
 edad int NOT NULL

);


CREATE DATA BASE Personas;

USE Personas;

CREATE TABLE empleado (
 id int PRIMARY KEY ,
 name char(5) NULL ,
 edad int NOT NULL,

);

CREATE TABLE manager (
 id int PRIMARY KEY ,
 name char(5) NULL ,
 edad int NOT NULL

);

USE Personas;

DROP TABLE manager