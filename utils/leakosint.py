import requests
import os
from dotenv import load_dotenv
from utils.dehashed import convert_json, print_debug

load_dotenv()
LEAKOSINT_API_KEY = os.getenv("LEAKSOSINT_API_KEY")

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
