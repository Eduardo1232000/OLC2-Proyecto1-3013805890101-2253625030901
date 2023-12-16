USE Alimentos;
CREATE PROCEDURE prueba (@var1 INT , @var2 INT , @var3 INT) 
AS
BEGIN
	DECLARE @IVA INT;

	SET @IVA = 3;

	@IVA +1

END

EXEC prueba 1,2,3

