CREATE DATABASE db

CREATE TABLE persona(
    id SERIAL PRIMARY KEY,
    dpi NVARCHAR (20) UNIQUE,
    first_name NVARCHAR(255)
);


INSERT INTO persona VALUES ('2253','paco');

DROP DATA BASE nombre_base;


USE perrito
DROP TABLE raza;

