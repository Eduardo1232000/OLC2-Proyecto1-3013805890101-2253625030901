CREATE DA´´TA BASE Personas;
USE Personas;

CREaATE TABLE Trabajador (
 id int PRIMARY KEY ,
 name nchar(50) NULL ,
 edad int NOT NULL,
 dpi nchar(13) NULL
);

CREATE TABLE Independiente (
 id int PRIMARY KEY ,
 name nchar(10) NOT NULL ,
 edad int NOT NULL,
 email nvarchar(20) NULL
);

INSERT INTO Trabajador (id, name, edad,dpi)
VALUES (1,"Eduardo",23,"dpi_prueba");





