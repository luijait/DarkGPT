import requests
import json
import sys
from dotenv import load_dotenv
load_dotenv()
import time
import os

# Carga de variables de entorno para autenticación en la API de Dehashed
DEHASHED_API_KEY = os.getenv("DEHASHED_API_KEY")
DEHASHED_USERNAME = os.getenv("DEHASHED_USERNAME")

def consultar_dominio_dehashed(consulta, debug=False):
    print(consulta)
    time.sleep(10)
    """
    Consulta información de un dominio específico a través de la API de Dehashed.
    
    Esta función construye los parámetros de consulta basados en la entrada del usuario, realiza la consulta a la API
    y procesa los resultados obtenidos para devolverlos en un formato legible.
    
    Args:
        consulta (dict): Un diccionario con los parámetros de consulta (por ejemplo, correo electrónico, nombre de usuario).
    
    Returns:
        str: Una cadena formateada con los resultados de la consulta.
    """
    parametros = {'email': consulta.get("mail"), 'username': consulta.get("nickname")}
    
    if debug:
        print(f"[DEBUG] Parámetros de consulta: {parametros}")
    
    resultados = {}
    headers = {'Accept': 'application/json'}
    
    # Realiza una consulta a la API para cada parámetro no nulo y acumula los resultados
    for tipo, valor in parametros.items():
        if valor:
            try:
                params = (('query', valor),)
                if debug:
                    print(f"[DEBUG] Consultando {tipo} con valor: {valor}")
                
                response = requests.get(
                    'https://api.dehashed.com/search',
                    headers=headers,
                    params=params,
                    auth=(DEHASHED_USERNAME, DEHASHED_API_KEY)
                )
                
                if debug:
                    print(f"[DEBUG] Respuesta cruda de Dehashed para {tipo}: {response.text}")
                
                json_crudo_dehashed = response.text
                resultados[tipo] = convertir_json(json_crudo_dehashed)
                
                if debug:
                    print(f"[DEBUG] Resultados después de convertir JSON para {tipo}: {resultados[tipo]}")
            except Exception as e:
                print(f"Error al consultar {tipo}: {e}")
                if debug:
                    print(f"[DEBUG] Excepción completa: {e}")
                pass
    
    # Formatea los resultados para su presentación
    resultado_ordenado = ""
    cabecera = "A continuación se muestran algunos de los registros encontrados:\n"
    
    if debug:
        print("[DEBUG] Formateando los resultados para la presentación.")
    
    for parametro, entradas in resultados.items():
        if isinstance(entradas, list):
            for item in entradas:
                if isinstance(item, dict):
                    fila = (
                        f"{item.get('email', 'No disponible')}, "
                        f"{item.get('username', 'No disponible')}, "
                        f"{item.get('password', 'No disponible')}, "
                        f"{item.get('hashed_password', 'No disponible')}, "
                        f"{item.get('phone', 'No disponible')}, "
                        f"{item.get('database_name', 'No disponible')}\n"
                    )
                    if debug:
                        print(f"[DEBUG] Fila formateada: {fila.strip()}")
                    resultado_ordenado += fila
                else:
                    if debug:
                        print(f"[DEBUG] Item no es un diccionario: {item}")
        else:
            if debug:
                print(f"[DEBUG] Entradas no es una lista: {entradas}")
    
    tabla_completa = cabecera + resultado_ordenado
    if debug:
        print(f"[DEBUG] Tabla completa:\n{tabla_completa}")
    else:
        print(resultado_ordenado)
    
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
    try:
        datos_json = json.loads(raw_json)
        if isinstance(datos_json, dict) and 'entries' in datos_json:
            return datos_json['entries']
        else:
            print("[DEBUG] La respuesta JSON no tiene el formato esperado")
            return []
    except json.JSONDecodeError:
        print("[DEBUG] Error al decodificar JSON")
        return []
