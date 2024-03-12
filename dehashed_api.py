import requests
import json
import sys
from dotenv import load_dotenv
load_dotenv()

import os

# Carga de variables de entorno para autenticación en la API de Dehashed
DEHASHED_API_KEY = os.getenv("DEHASHED_API_KEY")
DEHASHED_USERNAME = os.getenv("DEHASHED_USERNAME")

def consultar_dominio_dehashed(consulta):
    """
    Consulta información de un dominio específico a través de la API de Dehashed.
    
    Esta función construye los parámetros de consulta basados en la entrada del usuario, realiza la consulta a la API
    y procesa los resultados obtenidos para devolverlos en un formato legible.
    
    Args:
        consulta (dict): Un diccionario con los parámetros de consulta (por ejemplo, correo electrónico, nombre de usuario).
    
    Returns:
        str: Una cadena formateada con los resultados de la consulta.
    """
    parametros = []
    # Construye la lista de parámetros de consulta basada en la entrada proporcionada
    parametros = {'email': consulta.get("mail"), 'username': consulta.get("nickname")}
    
    resultados = {}
    headers = {'Accept': 'application/json',}
    
    # Realiza una consulta a la API para cada parámetro no nulo y acumula los resultados
    for tipo, valor in parametros.items():
        if valor:
            try:
                params = (('query', valor),)
                json_crudo_dehashed = requests.get('https://api.dehashed.com/search',
                                               headers=headers,
                                               params=params,
                                               auth=(DEHASHED_USERNAME, DEHASHED_API_KEY)).text
                
                resultados[tipo] = convertir_json(json_crudo_dehashed)
            except Exception as e:
                print(f"Error al consultar {tipo}: {e}")
                pass
    # Formatea los resultados para su presentación
    resultado_ordenado = ""
    import time
    cabecera = "A continuación se muestran algunos de los registros encontrados:\n"
    for parametro, entradas in resultados.items():
        for item in entradas:
            fila = f"{item.get('email', 'No disponible')}, "
            fila += f"{item.get('username', 'No disponible')}, "
            fila += f"{item.get('password', 'No disponible')}, "
            fila += f"{item.get('hashed_password', 'No disponible')}, "
            fila += f"{item.get('phone', 'No disponible')}, "
            fila += f"{item.get('database_name', 'No disponible')}\n"
            resultado_ordenado += fila
    tabla_completa = cabecera + resultado_ordenado
 
    return resultado_ordenado
def convertir_json(raw_json):
    """
    Convierte una cadena JSON cruda en una lista de objetos Python.
    
    Esta función es útil para procesar la respuesta de la API de Dehashed, convirtiendo la cadena JSON en una lista
    de diccionarios que representan las entradas individuales de la respuesta.
    
    Args:
        raw_json (str): La cadena JSON cruda.
        
    Returns:
        list: Una lista de diccionarios, cada uno representando una entrada de la respuesta.
    """
    datos_json = json.loads(raw_json)
    entradas = datos_json['entries']
    return entradas

