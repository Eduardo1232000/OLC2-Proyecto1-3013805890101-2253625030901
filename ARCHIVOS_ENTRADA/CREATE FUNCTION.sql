USE Alimentos;
CREATE FUNCTION prueba (@var1 INT , @var2 INT , @var3 INT, @var4 NCHAR(5), @var5 NVARCHAR(3)) 
RETURN INT
AS
BEGIN
	DECLARE @IVA INT;

	SET @IVA = 3;

	@IVA +1

END;






