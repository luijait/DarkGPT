import os
from darkgpt import GPT_with_function_output
from utils import print_debug
import argparse

# ANSI color codes
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"

def parse_arguments():
    parser = argparse.ArgumentParser(description="DarkGPT CLI")
    parser.add_argument("--api", choices=["dehashed", "leakosint"], default="leakosint", help="Choose the API to use")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    parser.add_argument("--shell", action="store_true", help="Start in interactive shell mode")
    parser.add_argument("message", nargs="?", help="Initial message for the conversation (ignored in shell mode)")
    return parser.parse_args()

def start_shell(darkgpt, api_choice, debug=False):
    print(f"{GREEN}Welcome to DarkGPT, the best OSINT Agent{RESET}")
    print(f"{YELLOW}A wizard that uses GPT-4 to do database queries and filtered information written by @luijait_.{RESET}")
    print(f"{YELLOW}Type 'exit' to finish, 'clear' to clear the screen.{RESET}")
    print(f"{YELLOW}Using {api_choice.upper()} API.{RESET}")
    print(f"{YELLOW}Twitter @luijait_{RESET}")

    try:
        while True:
            user_input = input(f"{GREEN}> {RESET}").strip()
            if user_input.lower() == 'exit':
                print(f"{YELLOW}Terminated the session.{RESET}")
                break
            elif user_input.lower() == 'clear':
                os.system('cls' if os.name == 'nt' else 'clear')
            else:
                process_input(darkgpt, user_input, api_choice, debug)
    except KeyboardInterrupt:
        print(f"\n{YELLOW}Session terminated by the user.{RESET}")

def process_input(darkgpt, user_input, api_choice, debug=False):
    def handle_chunk(chunk_content):
        print(chunk_content, end="")

    history = {"USUARIO": user_input}
    historial_json = [history]

    GPT_with_function_output(
        openai_client=darkgpt['client'],
        model_name=darkgpt['model_name'],
        temperature=darkgpt['temperature'],
        functions=darkgpt['functions'],
        agent_prompt=darkgpt['agent_prompt'],
        historial=historial_json,
        callback=handle_chunk,
        api_choice=api_choice,
        debug=debug
    )
    
    if debug:
        print_debug("Processed input and received response successfully.")
