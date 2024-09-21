import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()

# Load environment variables for Dehashed API authentication
DEHASHED_API_KEY = os.getenv("DEHASHED_API_KEY")
DEHASHED_USERNAME = os.getenv("DEHASHED_USERNAME")

def query_dehashed(query, size=100, page=1, debug=False):
    """
    Query the Dehashed API with the given parameters.
    
    Args:
        query (str): The search query.
        size (int): Number of results per page (default 100, max 10000).
        page (int): Page number for pagination (default 1).
        debug (bool): Enable debug logging.
    
    Returns:
        dict: The API response as a dictionary.
    """
    url = 'https://api.dehashed.com/search'
    headers = {'Accept': 'application/json'}
    params = {
        'query': query,
        'size': size,
        'page': page
    }
    
    if debug:
        print(f"[DEBUG] Query parameters: {params}")
    
    try:
        response = requests.get(
            url,
            headers=headers,
            params=params,
            auth=(DEHASHED_USERNAME, DEHASHED_API_KEY)
        )
        response.raise_for_status()
        
        if debug:
            print(f"[DEBUG] API response status code: {response.status_code}")
        
        return response.json()
    except requests.exceptions.RequestException as e:
        if debug:
            print(f"[DEBUG] API request error: {e}")
        return {"error": str(e)}

def format_results(api_response, debug=False):
    """
    Format the API response into a readable string.
    
    Args:
        api_response (dict): The API response dictionary.
        debug (bool): Enable debug logging.
    
    Returns:
        str: Formatted results string.
    """
    if 'entries' not in api_response:
        if debug:
            print("[DEBUG] No entries found in API response")
        return "No results found or error in API response."
    
    formatted_results = "Results:\n"
    for entry in api_response['entries']:
        formatted_results += (
            f"Email: {entry.get('email', 'N/A')}, "
            f"Username: {entry.get('username', 'N/A')}, "
            f"Password: {entry.get('password', 'N/A')}, "
            f"Hashed Password: {entry.get('hashed_password', 'N/A')}, "
            f"Phone: {entry.get('phone', 'N/A')}, "
            f"Database: {entry.get('database_name', 'N/A')}\n"
        )
    
    if debug:
        print(f"[DEBUG] Formatted {len(api_response['entries'])} results")
    
    return formatted_results

def search_dehashed(query, size=100, page=1, debug=False):
    """
    Search Dehashed API and return formatted results.
    
    Args:
        query (str): The search query.
        size (int): Number of results per page (default 100, max 10000).
        page (int): Page number for pagination (default 1).
        debug (bool): Enable debug logging.
    
    Returns:
        str: Formatted search results.
    """
    if debug:
        print(f"[DEBUG] Initiating Dehashed search with query: {query}")
    
    api_response = query_dehashed(query, size, page, debug)
    
    if 'error' in api_response:
        return f"Error querying Dehashed API: {api_response['error']}"
    
    formatted_results = format_results(api_response, debug)
    
    if debug:
        print(f"[DEBUG] Search completed. Total results: {api_response.get('total', 'Unknown')}")
    
    return formatted_results

