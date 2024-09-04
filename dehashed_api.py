from dotenv import load_dotenv
import requests
import json
load_dotenv()

import os

# Carga de variables de entorno para autenticación en la API de Dehashed
DEHASHED_API_KEY = os.getenv("DEHASHED_API_KEY")
DEHASHED_USERNAME = os.getenv("DEHASHED_USERNAME")

def check_domain_info_dehashed(request_dict: dict) -> str:
    """
    Gets the domain information by using Dehashed API, it builds the parameters making use of 
    user input and then makes the request.

    :param request_dict: Dict that contains the request  

    """

    params = {'email': request_dict.get("mail"), 'username': request_dict.get("nickname")}
    
    results = {}
    headers = {'Accept': 'application/json',}
    
    for param_key, param_value in params.items():
        if not param_value:
            continue

        try:
            inside_params = (('query', param_value),)
            response = requests.get('https://api.dehashed.com/search',
                                           headers=headers,
                                           params=inside_params,
                                           auth=(DEHASHED_USERNAME, DEHASHED_API_KEY)).text
            
            results[param_key] = parse_json(response)
        except requests.exceptions.HTTPError:
            print(f"Se ha producido un error con la respuesta. (HTTPError). Ignorando...")
            continue

    ordered = ""
    header = "A continuación se muestran algunos de los registros encontrados:\n"
    for inputs in results.values():
        for item in inputs:
            ordered = f"{item.get('email', 'No disponible')}, "
            ordered += f"{item.get('username', 'No disponible')}, "
            ordered += f"{item.get('password', 'No disponible')}, "
            ordered += f"{item.get('hashed_password', 'No disponible')}, "
            ordered += f"{item.get('phone', 'No disponible')}, "
            ordered += f"{item.get('database_name', 'No disponible')}\n"
 
    return  header + ordered


def parse_json(raw_json):
    """
    Parses raw json response from the request 
    :param raw_json: The raw json response
    """
    json_data = json.loads(raw_json)
    return json_data["entries"]

