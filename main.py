# Importación de módulos necesarios
import os
import argparse
from darkgpt import print_debug
from cli import start_shell
from openai import Client
from dotenv import load_dotenv
import os
from functions import Leak_Function

load_dotenv()

# Banner de inicio para la aplicación, mostrando un diseño ASCII con el creador
banner = """
________       __        _______   __   ___       _______    _______  ___________  
|"      "\     /""\      /"      \ |/"| /  ")     /" _   "|  |   __ "\("     _   ") 
(.  ___  :)   /    \    |:        |(: |/   /     (: ( \___)  (. |__) :))__/  \\__/  
|: \   ) ||  /' /\  \   |_____/   )|    __/       \/ \       |:  ____/    \\_ /     
(| (___\ || //  __'  \   //      / (// _  \       //  \ ___  (|  /        |.  |     
|:       :)/   /  \\  \ |:  __   \ |: | \  \     (:   _(  _|/|__/ \       \:  |     
(________/(___/    \___)|__|  \___)(__|  \__)     \_______)(_______)       \__|     

hecho por: @luijait_
ayudado por: @simplyjuanjo (juanjeras)
"""
# Imprimir el banner para dar la bienvenida al usuario
print(banner)

# Definición de la función principal
def main():
    # Configurar el parser de argumentos
    parser = argparse.ArgumentParser(description="DarkGPT CLI")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    args = parser.parse_args()

    # ANSI escape codes for colored output
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    RESET = "\033[0m"

    def print_debug(message, is_error=False, is_warning=False):
        color = RED if is_error else (YELLOW if is_warning else GREEN)
        print(f"{color}[DEBUG] {message}{RESET}")

    # Check for required API keys
    if not os.getenv("OPENAI_API_KEY"):
        print_debug("WARNING: OPENAI_API_KEY not found in environment variables.", is_warning=True)
        print_debug("CRITICAL: OpenAI API key is missing. The application will not function correctly without this.", is_error=True)
        print_debug("Please set OPENAI_API_KEY in your .env file.", is_error=True)
        return

    if not os.getenv("DEHASHED_API_KEY") or not os.getenv("DEHASHED_USERNAME"):
        print_debug("WARNING: DEHASHED_API_KEY or DEHASHED_USERNAME not found in environment variables.", is_warning=True)
        print_debug("CRITICAL: DeHashed API credentials are missing. The application will not function correctly without these.", is_error=True)
        print_debug("Please set DEHASHED_API_KEY and DEHASHED_USERNAME in your .env file.", is_error=True)
        return

    darkgpt = {
        "client": Client(api_key=os.getenv("OPENAI_API_KEY")),
        "model_name": os.getenv("GPT_MODEL_NAME"),
        "temperature": 0.0,
        "functions": Leak_Function,
        "agent_prompt": """You are an AI assistant specialized in OSINT (Open Source Intelligence) and information gathering. Your task is to analyze the provided data and give insights based on the leaked information found. Please be factual and objective in your analysis. Do not engage in or encourage any illegal activities. Respect privacy and use information ethically.

Given the following leaked data: {}

Please provide a detailed analysis including:
1. Overview of the data leaked
2. Potential security implications
3. Recommendations for affected parties
4. General cybersecurity best practices

Format your response in a clear, professional manner.
Create a complex markdown table with every leak
"""
    }

    start_shell(darkgpt, debug=args.debug)

    if args.debug:
        print_debug("DarkGPT and ConversationalShell initialized with debug mode enabled.")

# Punto de entrada principal para ejecutar la aplicación
if __name__ == "__main__":
    main()
