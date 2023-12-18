USE Prueba_archivo;

CREATE TABLE tabla1 (
numero1 int,
numero2 decimal,
valor1 nchar(5) ,
valor2 nvarchar(5),
fecha1 date,
fecha2 datetime
);

CREATE TABLE tabla2 (
numero1 int PRIMARY KEY,
numero2 decimal NULL,
valor1 nchar(5)  NOT NULL,
valor2 nvarchar(5) NOT NULL,
fecha1 date NULL,
fecha2 datetime NULL
);

CREATE TABLE tabla3 (
id int primary key,
numero1 int ,
numero2 decimal NULL,
valor1 nchar(5)  NOT NULL,
valor2 nvarchar(5) NOT NULL,
fecha1 date NULL,
fecha2 datetime NULL,
FOREIGN KEY(numero1) REFERENCE tabla2(numero1)
);








