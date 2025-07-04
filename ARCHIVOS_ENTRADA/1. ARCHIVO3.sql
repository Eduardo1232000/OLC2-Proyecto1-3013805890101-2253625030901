use cali;

CREATE FUNCTION fn_retornaalturamora (@diasmora int)
RETURN nvarchar(100)
AS
BEGIN
	DECLARE @alturamora nvarchar(100);
		IF (@diasmora > 0) && (@diasmora < 30) 
		THEN
			SET @alturamora = 'Al dia';
		END IF;
	
		IF (@diasmora >= 30) && (@diasmora < 60) 
		THEN
			SET @alturamora = 'Altura Mora 2';	
		END IF;
	
		IF (@diasmora >= 30) && (@diasmora < 60) 
		THEN
			SET @alturamora = 'Altura Mora 3';				
		END IF;

		IF (@diasmora >= 60) && (@diasmora < 90) 
		THEN
			SET @alturamora = 'Altura Mora 4';		
		END IF;
	
		IF (@diasmora >= 90) && (@diasmora < 120) 
		THEN
			SET @alturamora = 'Altura Mora 5';				
		END IF;
	RETURN @alturamora;
END;

CREATE PROCEDURE sp_actualizaalturamora (@credito int,@diasmora int)
AS
BEGIN
	DECLARE @alturamora int	;
		IF (@diasmora > 0) && (@diasmora < 30) 
		THEN
			SET @alturamora = 0;
		END IF;
	
		IF (@diasmora >= 30) && (@diasmora < 60) 
		THEN
			SET @alturamora = 1;	
		END IF;
	
		IF (@diasmora >= 30) && (@diasmora < 60) 
		THEN
			SET @alturamora = 2;				
		END IF;

		IF (@diasmora >= 60) && (@diasmora < 90) 
		THEN
			SET @alturamora = 3;		
		END IF;
	
		IF (@diasmora >= 90) && (@diasmora < 120) 
		THEN 
			SET @alturamora = 4;				
		END IF;
	             
		update tbcreditosaldo set alturamora = @alturamora ;
		where credito = @credito and diasmora = @diasmora;
		
END;

CREATE FUNCTION sp_calculacuota (@saldo decimal, @plazo int ,@diasmora int)
RETURN decimal
AS
BEGIN
		DECLARE @cuota decimal;
		DECLARE @ajuste decimal ;
		
		if (@saldo > 5000) && (@diasmora > 30)
		then
			set @cuota = (@saldo/@plazo)*0.45;
		END IF;
	
		if (@saldo > 15000) && (@diasmora > 30) 
		then
			set @cuota = (@saldo/@plazo)*0.65;	
		END IF;

		if (@saldo > 25000) && (@diasmora > 60) 
		THEN
			set @cuota = (@saldo/@plazo)*0.70;			
		END IF;
	
		if (@saldo < 15000) && (@diasmora < 30) 
		THEN
			set @cuota = (@saldo/@plazo)*0.15;			
		END IF;
	
		CASE WHEN (@cuota > 1000) && (@cuota <  1500)
				THEN SET @ajuste = 75;
			WHEN @cuota >= 1500 && @cuota <  2000
				THEN SET @ajuste = 125;	
			WHEN @cuota > 0 &&  @cuota < 1000
				THEN SET @ajuste = 25;
			WHEN @cuota >=  2000
				THEN SET @ajuste = 150;					
			ELSE 
				THEN SET @ajuste = 0;
		END;
		
		SET @cuota = @cuota-@ajuste;	
			
		RETURN @cuota;	
		
		
END;




