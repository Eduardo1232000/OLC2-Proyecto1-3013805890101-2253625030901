import xml.etree.ElementTree as ET
import xml.dom.minidom
import os
from FUNCIONES.ARBOL.VALOR import *

def seleccionar_datos(base_activa, tabla, columnas, condiciones):
    
    try:
        print(condiciones)
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
                    fila_resultado = [valor.text for valor in dato.findall('valor')]
                    

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

    valores_fila = [valor.text for valor in dato.findall('valor')]
    #print(f"VALORES FILA: {valores_fila}")

    for i in range(0, len(condiciones), 3):
        columna = condiciones[i]
        operador = condiciones[i + 1]
        valor_condicion = condiciones[i + 2]

        # Obtenemos el nombre de la columna, el operador y el valor de la condición
        columna_nombre = columna if isinstance(columna, str) else columna.text
        operador = operador if isinstance(operador, str) else operador.text
        valor_condicion = valor_condicion if isinstance(valor_condicion, str) else valor_condicion.text


        #print(f"COLUMNA: {columna_nombre}")
        #print(f"Operador: {operador}")
        #print(f"VALOR: {valor_condicion}")

        # Obtenemos el índice del campo relacionado con la columna
        #print("Contenido de dato:", ET.tostring(dato))

        indice_valor = None
        for j, valor in enumerate(dato.findall('valor')):
            print("ENTRE AL CICLO FOR")
            if valor.text == valor_condicion:
                indice_valor = j
                print(f"indice_campo: {j}")
                break

        if indice_valor is not None:
            # Obtenemos el valor relacionado con el campo
            valor_actual = valores_fila[indice_valor]
            print(f"Valor_actual: {valor_actual}")

            # Realizamos las comparaciones según el operador
            if operador == '=' and valor_actual == valor_condicion:
                continue
            elif operador == '<' and valor_actual < valor_condicion:
                continue
            elif operador == '>' and valor_actual > valor_condicion:
                continue

        # Si no se cumple alguna condición, retorna False
        return False

    return True  # Todas las condiciones se cumplieron
