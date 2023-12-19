import xml.etree.ElementTree as ET
import xml.dom.minidom
import os
from FUNCIONES.ARBOL.VALOR import *

def seleccionar_datos(base_activa, tabla, columnas, condiciones):
    
    try:
        ruta= "BASE_DATOS/" + str(base_activa)+ ".xml"
        tree = ET.parse(ruta)
        root = tree.getroot()

        tabla_existente = None
        for base in root.findall('base'):
            if base.attrib['name'] == base_activa:
                for tabla_xml in base:
                    nombre_tabla = tabla_xml.attrib['name']
                    if nombre_tabla == tabla:
                        tabla_existente = tabla_xml
                        break
                    if tabla_existente is not None:
                        break

        if tabla_existente is not None:
            if columnas == ['*']:
                campos_resultado = []
                datos_resultado = []

                for campo in tabla_existente.findall('campo'):
                    campos_resultado.append(campo.find('nombre').text)
                
                for dato in tabla_existente.findall('dato'):
                    fila_resultado = []
                    #cumple_condiciones = True

                    for valor in dato:
                        fila_resultado.append(valor.text)
                        
                        #datos_resultado.append(fila_resultado)

                    if cumple_condiciones(dato, condiciones):
                        datos_resultado.append(fila_resultado)
                

                return campos_resultado, datos_resultado
            
            else:
                    
                pass
        
        else:
            print(f"Error: la tabla {tabla} no existe en DB")

    except Exception as e:
        print(f"Error al ejecutar la SELECCION: {type(e).__name__} - {e}\n")




def cumple_condiciones(dato, condiciones):
    if not condiciones:
        return True  # Si no hay condiciones, siempre cumple

    valores_fila =[valor.text for valor in dato.findall('valor')]
    #valores_fila =[valor.text for valor in dato]
    
    # Crear un diccionario para almacenar los valores de cada columna
    #valores_fila = {valor.find('nombre').text: valor.text for valor in dato.findall('valor')}
    


    # Evaluar cada condición en la fila de datos
    for i in range(0, len(condiciones), 3):
        columna = condiciones[i]
        operador = condiciones[i + 1]
        valor_condicion = condiciones[i + 2]

        valor_actual = valores_fila[i // 3]
        #valor_actual = valores_fila.get(columna)


        # Comparar valores según el operador
        if operador == '=' and valor_actual == valor_condicion:
            continue
        elif operador == '<' and valor_actual < valor_condicion:
            continue
        elif operador == '>' and valor_actual > valor_condicion:
            continue
        # Añade más comparaciones según sea necesario

        # Si no se cumple alguna condición, retorna False
        return False

    return True  # Todas las condiciones se cumplieron