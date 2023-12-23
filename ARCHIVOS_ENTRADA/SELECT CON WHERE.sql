Use Alimentos;
select * from products where product_no >1;
SELECT name, CONCATENA(id_producto,"B") VALIDACION from products where product_no >=1;
select name, product_no from products where (product_no >1) || (name == "Manza2");
