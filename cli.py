import os
from darkgpt import DarkGPT
from utils.dehashed import print_debug
import argparse

# ANSI color codes
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"

def parse_arguments():
    parser = argparse.ArgumentParser(description="DarkGPT CLI")
    parser.add_argument("--api", choices=["dehashed", "leakosint"], default="leakosint", help="Choose the API to use")
    parser.add_argument("--debug", default=False, action="store_true", help="Enable debug mode")
    parser.add_argument("--shell", default=False, action="store_true", help="Start in interactive shell mode")
    parser.add_argument("--log", default=True, action="store_true", help="Enable logging mode")
    parser.add_argument("--temperature", type=float, default=0.7, help="Set the temperature for the model")
    parser.add_argument("--agent-prompt", type=str, help="Path to the agent prompt file")
    parser.add_argument("--enable-ollama", default=False, action="store_true", help="Enable Ollama API")
    parser.add_argument("--model", help="Set the model to use")
    parser.add_argument("--openai-api-key", help="Set the OpenAI API key to use")
    parser.add_argument("--dehashed-api-key", help="Set the Dehashed API key to use")
    parser.add_argument("--dehashed-username", help="Set the Dehashed username to use")
    parser.add_argument("--leakosint-api-key", help="Set the Leakosint API key to use")
    parser.add_argument("message", nargs="?", help="Initial message for the conversation (ignored in shell mode)")
    return parser.parse_args()

def start_shell(darkgpt, api_choice, debug=False):
    print(f"{GREEN}Welcome to DarkGPT, the best OSINT Agent{RESET}")
    print(f"{YELLOW}A wizard that uses GPT-4o to do database queries and filtered information written by @luijait_.{RESET}")
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
                init_shell(darkgpt, user_input, api_choice, debug)
    except KeyboardInterrupt:
        print(f"\n{YELLOW}Session terminated by the user.{RESET}")

def init_shell(darkgpt, user_input, api_choice, debug=False):
    user_prompt = [{"role": "user", "content": user_input}]
    darkgpt.run(user_prompt)

