USE Prueba_archivo;

DECLARE @var1 as int;
DECLARE @var2 int;
SET @var1 = 5;
SET @var2 = @var1 + @var1;

CREATE PROCEDURE procedure1
AS
BEGIN 
	DECLARE @VALOR1 INT;
	SET @VALOR1= @var1;
	SELECT procedure1;
	SELECT @VALOR1;

END;

CREATE PROCEDURE procedure2 (@var1 INT) 
AS
BEGIN
	DECLARE @VALOR1 INT;
	SET @VALOR1= @var1;
END;








