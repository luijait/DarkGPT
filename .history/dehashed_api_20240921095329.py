import requests
import json
import sys
from dotenv import load_dotenv
import time
import os

load_dotenv()

# Load environment variables for Dehashed API authentication
DEHASHED_API_KEY = os.getenv("DEHASHED_API_KEY")
DEHASHED_USERNAME = os.getenv("DEHASHED_USERNAME")


def query_dehashed_domain(query, debug=False):
    parameters = {'email': query.get("mail"), 'username': query.get("nickname")}

    if debug:
        print(f"[DEBUG] Query parameters: {parameters}")

    results = {}
    headers = {'Accept': 'application/json'}

    # Query the API for each non-null parameter and accumulate the results
    for param_type, value in parameters.items():
        if value:
            try:
                params = (('query', value),)
                if debug:
                    print(f"[DEBUG] Querying {param_type} with value: {value}")

                response = requests.get(
                    'https://api.dehashed.com/search',
                    headers=headers,
                    params=params,
                    auth=(DEHASHED_USERNAME, DEHASHED_API_KEY)
                )

                if debug:
                    print(f"[DEBUG] Raw Dehashed response for {param_type}: {response.text}")

                raw_dehashed_json = response.text
                results[param_type] = convert_json(raw_dehashed_json)

                if debug:
                    print(f"[DEBUG] Results after converting JSON for {param_type}: {results[param_type]}")
            except Exception as e:
                print(f"Error querying {param_type}: {e}")
                if debug:
                    print(f"[DEBUG] Full exception: {e}")

    ordered_result = ""
    header = "Here are some of the records found:\n"

    if debug:
        print("[DEBUG] Formatting results for presentation.")

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
                        print(f"[DEBUG] Formatted row: {row.strip()}")
                    ordered_result += row
                else:
                    if debug:
                        print(f"[DEBUG] Item is not a dictionary: {item}")
        else:
            if debug:
                print(f"[DEBUG] Entries is not a list: {entries}")

    complete_table = header + ordered_result
    if debug:
        print(f"[DEBUG] Complete table:\n{complete_table}")

    if not ordered_result:
        print("No leaks found.")
        time.sleep(10)
    else:
        print(ordered_result)

    return ordered_result


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
