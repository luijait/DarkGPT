import requests
import json
import sys
import os

from dotenv import load_dotenv

# Carga las variables de entorno desde el archivo .env
load_dotenv()

# Acceder a las variables de entorno
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DEHASHED_API_KEY = os.getenv("DEHASHED_API_KEY")
DEHASHED_USERNAME = os.getenv("DEHASHED_USERNAME")

# Ahora puedes usar las variables, por ejemplo, para configurar clientes de API
print(OPENAI_API_KEY)
# Load environment variables for authentication with the Dehashed API
DEHASHED_API_KEY = os.getenv("DEHASHED_API_KEY")
DEHASHED_USERNAME = os.getenv("DEHASHED_USERNAME")

def query_dehashed_domain(query):
    """
    Queries specific domain information through the Dehashed API.
    
    This function constructs the query parameters based on user input, performs the query to the API,
    and processes the obtained results to return them in a readable format.
    
    Args:
        query (dict): A dictionary with the query parameters (e.g., email, username).
    
    Returns:
        str: A formatted string with the query results.
    """
    parameters = {'email': query.get("mail"), 'username': query.get("nickname")}
    
    results = {}
    headers = {'Accept': 'application/json',}
    
    # Perform a query to the API for each non-null parameter and accumulate the results
    for type, value in parameters.items():
        if value:
            try:
                params = (('query', value),)
                raw_json_dehashed = requests.get('https://api.dehashed.com/search',
                                               headers=headers,
                                               params=params,
                                               auth=(DEHASHED_USERNAME, DEHASHED_API_KEY)).text
                
                results[type] = convert_json(raw_json_dehashed)
            except Exception as e:
                print(f"Error querying {type}: {e}")
                pass
    # Format the results for presentation
    formatted_result = ""
    header = "Below are some of the records found:\n"
    for parameter, entries in results.items():
        for item in entries:
            row = f"{item.get('email', 'Not available')}, "
            row += f"{item.get('username', 'Not available')}, "
            row += f"{item.get('password', 'Not available')}, "
            row += f"{item.get('hashed_password', 'Not available')}, "
            row += f"{item.get('phone', 'Not available')}, "
            row += f"{item.get('database_name', 'Not available')}\n"
            formatted_result += row
    complete_table = header + formatted_result
    return formatted_result

def convert_json(raw_json):
    """
    Converts a raw JSON string into a list of Python objects.
    
    This function is useful for processing the response from the Dehashed API, converting the JSON string into a list
    of dictionaries representing the individual entries in the response.
    
    Args:
        raw_json (str): The raw JSON string.
        
    Returns:
        list: A list of dictionaries, each representing an entry in the response.
    """
    json_data = json.loads(raw_json)
    entries = json_data['entries']
    return entries
