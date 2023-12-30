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
genero NVARCHAR(1) NULL ,
idestado INT NOT NULL REFERENCE tbestado(idestado)
);

CREATE TABLE tbidentificacion (
ididentificacion INT NOT NULL PRIMARY KEY ,
codigocliente NVARCHAR(15) NOT NULL PRIMARY KEY REFERENCE tbcliente(codigocliente),
identificacion NVARCHAR(20) NOT NULL ,
ididentificaciontipo INT NULL REFERENCE tbidentificaciontipo(ididentificaciontipo)
);

CREATE TABLE tbproducto (
idproducto INT NOT NULL PRIMARY KEY ,
producto NVARCHAR(100) NOT NULL ,
idestado INT NOT NULL ,
tasa DECIMAL NOT NULL REFERENCE False(None)
);

CREATE TABLE tbcredito (
credito INT NOT NULL PRIMARY KEY ,
nocuenta NVARCHAR(20) NOT NULL ,
idcliente INT NOT NULL ,
fechaultimocorte DATE NOT NULL ,
idproducto INT NULL REFERENCE tbproducto(idproducto)
);

CREATE TABLE tbobligaciontipo (
idobligaciontipo INT NOT NULL PRIMARY KEY ,
obligaciontipo NVARCHAR(30) NULL 
);

CREATE TABLE tbcreditoobligacion (
codigocliente NVARCHAR(15) NOT NULL PRIMARY KEY ,
credito INT NOT NULL PRIMARY KEY ,
idobligaciontipo INT NULL REFERENCE tbobligaciontipo(idobligaciontipo)
);

CREATE TABLE tbcreditoSaldo (
credito INT NOT NULL PRIMARY KEY ,
fechacorte DATE NOT NULL PRIMARY KEY ,
idmoneda INT NOT NULL PRIMARY KEY ,
idcreditoestado INT NOT NULL PRIMARY KEY ,
SaldoActual DECIMAL NULL ,
SaldoMora DECIMAL NULL ,
ValorCuota DECIMAL NULL ,
DiasMora INT NULL ,
alturamora INT NOT NULL ,
limite DECIMAL NOT NULL ,
idcalificacion INT NOT NULL 
);

CREATE FUNCTION fn_retornanombre(@identificacion NVARCHAR(20), @primernombre NVARCHAR(20), @segundonombre NVARCHAR(20))
RETURN NVARCHAR(100)
AS
BEGIN
	DECLARE @nombres nvarchar(100);
	DECLARE @apellidos nvarchar(100);
	DECLARE @nombrecompleto nvarchar(100);
	set @nombres = CONCATENA(@primer_nombre, @segundo_nombre);
	set @APELLIDOS = CONCATENA(@primer_nombre, @segundo_nombre);
	set @nombrecompleto = CONCATENA(@nombrecompleto, @apellidos);
	return @nombrecompleto;

END;

