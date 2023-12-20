CREATE DATA BASE tbbanco;

USE tbbanco;

CREATE TABLE tbestado (
idestado INT NOT NULL PRIMARY KEY ,
estado NVARCHAR(50) NOT NULL 
);

CREATE TABLE tbidentificaciontipo (
ididentificaciontipo INT NOT NULL PRIMARY KEY ,
identificaciontipo NVARCHAR(15) NOT NULL 
);

CREATE TABLE tbcliente (
codigocliente NVARCHAR(15) NOT NULL PRIMARY KEY ,
primer_nombre NVARCHAR(50) NOT NULL ,
segundo_nombre NVARCHAR(50) NULL ,
primer_apellido NVARCHAR(50) NOT NULL ,
segundo_apellido NVARCHAR(50) NULL ,
fecha_nacimiento DATE NOT NULL ,
genero NVARCHAR(50) NULL ,
idestado INT NOT NULL REFERENCE tbestado(idestado)
);

CREATE TABLE tbidentificacion (
ididentificacion INT NOT NULL PRIMARY KEY ,
codigocliente NVARCHAR(15) NULL REFERENCE tbcliente(codigocliente),
identificacion NVARCHAR(20) NOT NULL ,
ididentificaciontipo INT NULL REFERENCE tbidentificaciontipo(ididentificaciontipo)
);

