import requests
import json
import sys
from dotenv import load_dotenv
import time
import os

load_dotenv()

# ANSI escape codes for colored output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"

def print_debug(message, is_error=False, is_warning=False):
    color = RED if is_error else (YELLOW if is_warning else GREEN)
    print(f"{color}[DEBUG] {message}{RESET}")

# Load environment variables for Dehashed API authentication
DEHASHED_API_KEY = os.getenv("DEHASHED_API_KEY")
DEHASHED_USERNAME = os.getenv("DEHASHED_USERNAME")
LEAKOSINT_API_KEY = os.getenv("LEAKSOSINT_API_KEY")


def convert_json(raw_json):
    """
    Converts a raw JSON string into a list of Python objects.

    This function is useful for processing the Dehashed API response,
    converting the JSON string into a list of dictionaries representing
    individual entries from the response.

    Args:
        raw_json (str): The raw JSON string.

    Returns:
        list: A list of dictionaries, each representing an entry from the response.
    """
    try:
        json_data = json.loads(raw_json)
        if isinstance(json_data, dict) and 'entries' in json_data:
            return json_data['entries']
        else:
            print("[DEBUG] The JSON response doesn't have the expected format")
            return []
    except json.JSONDecodeError:
        print("[DEBUG] Error decoding JSON")
        return []


def query_dehashed(queries, debug=False):

    
    if not DEHASHED_API_KEY or not DEHASHED_USERNAME:
        print_debug("WARNING: DEHASHED_API_KEY or DEHASHED_USERNAME not found in environment variables.", is_warning=True)
        print_debug("CRITICAL: DeHashed API credentials are missing. The application will not function correctly without these.", is_error=True)
        print_debug("Please set DEHASHED_API_KEY and DEHASHED_USERNAME in your .env file.", is_error=True)
        raise EnvironmentError("DEHASHED_API_KEY and DEHASHED_USERNAME must be set in the .env file.")

    if debug:
        print_debug("Starting query_dehashed function.")
    

    print_debug("Warning: The quality of responses depends on the accuracy of the provided queries and the DeHashed API's data.", is_warning=True)
    
    headers = {'Accept': 'application/json'}
    results = {}
    ordered_result = ""
    header = "Here are some of the records found:\n"

    if isinstance(queries, list):
        for i, query in enumerate(queries):
            if debug:
                print_debug(f"Processing query {i+1}: {query}")
            parameters = {'email': query.get("mail"), 'username': query.get("nickname")}
            if debug:
                print_debug(f"Query parameters: {parameters}")
            for param_type, value in parameters.items():
                if value:
                    try:
                        params = (('query', value),)
                        if debug:
                            print_debug(f"Querying {param_type} with value: {value}")
                        response = requests.get(
                            'https://api.dehashed.com/search',
                            headers=headers,
                            params=params,
                            auth=(DEHASHED_USERNAME, DEHASHED_API_KEY)
                        )
                        if debug:
                            print_debug(f"Raw Dehashed response for {param_type}: {response.text}")
                        raw_dehashed_json = response.text
                        results[param_type] = convert_json(raw_dehashed_json)
                        if debug:
                            print_debug(f"Results after converting JSON for {param_type}: {results[param_type]}")
                        if "Invalid API credentials" in raw_dehashed_json:
                            print_debug(f"{RED}ERROR: Invalid API credentials. Please check your DEHASHED_API_KEY and DEHASHED_USERNAME.{RESET}", is_error=True)
                            return None
                    except Exception as e:
                        print_debug(f"Error querying {param_type}: {e}", is_error=True)
                        if debug:
                            print_debug(f"Full exception: {e}", is_error=True)
    elif isinstance(queries, dict):
        query = queries
        if debug:
            print_debug("Processing single query.")
        parameters = {'email': query.get("mail"), 'username': query.get("nickname")}
        if debug:
            print_debug(f"Query parameters: {parameters}")
        for param_type, value in parameters.items():
            if value:
                try:
                    params = (('query', value),)
                    if debug:
                        print_debug(f"Querying {param_type} with value: {value}")
                    response = requests.get(
                        'https://api.dehashed.com/search',
                        headers=headers,
                        params=params,
                        auth=(DEHASHED_USERNAME, DEHASHED_API_KEY)
                    )
                    if debug:
                        print_debug(f"Raw Dehashed response for {param_type}: {response.text}")
                    raw_dehashed_json = response.text
                    results[param_type] = convert_json(raw_dehashed_json)
                    if debug:
                        print_debug(f"Results after converting JSON for {param_type}: {results[param_type]}")
                    # Check for invalid API credentials
                    if "Invalid API credentials" in raw_dehashed_json:
                        print_debug(f"{RED}ERROR: Invalid API credentials. Please check your DEHASHED_API_KEY and DEHASHED_USERNAME.{RESET}", is_error=True)
                        return None
                except Exception as e:
                    print_debug(f"Error querying {param_type}: {e}", is_error=True)
                    if debug:
                        print_debug(f"Full exception: {e}", is_error=True)
    else:
        print_debug("Invalid type for queries. Must be a dict or a list of dicts.", is_error=True)
        return ""
    
    if debug:
        print_debug("[DEBUG] Formatting results for presentation.")
    
    for parameter, entries in results.items():
        if isinstance(entries, list):
            for item in entries:
                if isinstance(item, dict):
                    row = (
                        f"{item.get('email', 'Not available')}, "
                        f"{item.get('username', 'Not available')}, "
                        f"{item.get('password', 'Not available')}, "
                        f"{item.get('hashed_password', 'Not available')}, "
                        f"{item.get('phone', 'Not available')}, "
                        f"{item.get('database_name', 'Not available')}\n"
                    )
                    if debug:
                        print_debug(f"[DEBUG] Formatted row: {row.strip()}")
                    ordered_result += row
                else:
                    if debug:
                        print_debug(f"[DEBUG] Item is not a dictionary: {item}")
        else:
            if debug:
                print_debug(f"[DEBUG] Entries is not a list: {entries}")
    
    complete_table = header + ordered_result
    if debug:
        print_debug(f"[DEBUG] Complete table:\n{complete_table}")
    
    if not ordered_result:
        print("No leaks found.")
        time.sleep(10)
    else:
        print(ordered_result)
    
    return ordered_result
def query_leakosint(queries, limit=100, lang='en', type='json', bot_name=None, debug=False):
    """
    Query the LeakOSINT API to obtain leak data for multiple queries.

    Parameters:
        queries (list or dict or str): Search queries in dict format with "nickname" or "mail" keys, 
                                     or a string query that will be searched as nickname
        limit (int, optional): Search limit (10 to 10000). Default is 100.
        lang (str, optional): Language code for results. Default is 'en'.
        type (str, optional): Report type ('json', 'short', 'html'). Default is 'json'.
        bot_name (str, optional): Bot name in format @name. Default is None.
        debug (bool, optional): Enable debug mode. Default is False.

    Returns:
        dict: API response data for all queries.
    """
    token = os.getenv("LEAKOSINT_API_KEY")
    if not token:
        print_debug("WARNING: LeakOSINT API token not provided.", is_warning=True)
        print_debug("CRITICAL: LeakOSINT API credentials are missing. The application will not function correctly without these.", is_error=True)
        print_debug("Please set LEAKOSINT_API_KEY in your .env file.", is_error=True)
        raise EnvironmentError("LeakOSINT API token must be provided either through the parameter or the .env file.")

    url = 'https://server.leakosint.com/'
    headers = {'Content-Type': 'application/json'}
    results = {}

    # Handle string query
    if isinstance(queries, str):
        # Treat string as nickname query
        query = {"nickname": queries}
        queries = [query]
    
    # Handle single dict query
    elif isinstance(queries, dict):
        queries = [queries]  # Convert to list for uniform processing

    # Handle list of queries
    if isinstance(queries, list):
        for i, query in enumerate(queries):
            # Convert string items in list to nickname queries
            if isinstance(query, str):
                query = {"nickname": query}
            
            if not isinstance(query, dict):
                print_debug(f"Invalid query format for item {i}", is_error=True)
                continue

            # Ensure query has either nickname or mail
            if not query.get("nickname") and not query.get("mail"):
                print_debug(f"Query must contain 'nickname' or 'mail' key: {query}", is_error=True)
                continue

            data = {
                'token': token,
                'request': query.get("nickname") or query.get("mail"),
                'limit': limit,
                'lang': lang,
            }

            if bot_name:
                data['bot_name'] = bot_name

            if debug:
                print_debug(f"Sending request to LeakOSINT API with data: {data}")

            try:
                response = requests.post(url, json=data, headers=headers, verify=False)
                if debug:
                    print_debug(f"Received response: {response.status_code} - {response.text}")
                response.raise_for_status()
                results[f"query_{i+1}"] = response.json()

            except requests.exceptions.HTTPError as http_err:
                if debug:
                    print_debug(f"HTTP error occurred: {http_err}", is_error=True)
                results[f"query_{i+1}"] = {'error': str(http_err)}
            except Exception as err:
                if debug:
                    print_debug(f"Other error occurred: {err}", is_error=True)
                results[f"query_{i+1}"] = {'error': str(err)}
    else:
        print_debug("Invalid type for queries. Must be a string, dict or list.", is_error=True)
        return {'error': 'Invalid query format'}

    if debug:
        print_debug(f"Final results: {results}")
    return results
