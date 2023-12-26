USE Alimentos;

SELECT 5;
SELECT CONCATENA("A","B");
Select * FROM products;
select * from products,Identificaciones;
SELECT name from products;
select name,id_producto from products;
select name,id_producto,Identificaciones.name from products,Identificaciones;
SELECT name, CONCATENA(id_producto,"B") from products;
SELECT name, CONCATENA(id_producto,"B") VALIDACION from products;
