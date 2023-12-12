CREATE DATABASE db

CREATE TABLE persona(
    id SERIAL PRIMARY KEY,
    dpi VARCHAR (20) UNIQUE,
    first_name VARCHAR(255)
);


INSERT INTO persona VALUES ('2253','paco');

DROP DATA BASE nombre_base;


USE perrito
DROP TABLE raza;

