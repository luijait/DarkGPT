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
ayudado por: @simplyjuanjo
"""
# Imprimir el banner para dar la bienvenida al usuario
print(banner)

# Definición de la función principal
def main():
    # Configurar el parser de argumentos
    parser = argparse.ArgumentParser(description="DarkGPT CLI")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    args = parser.parse_args()

    darkgpt = {
        "client": Client(api_key=os.getenv("OPENAI_API_KEY")),
        "model_name": os.getenv("GPT_MODEL_NAME"),
        "temperature": 0.7,
        "functions": Leak_Function,
        "agent_prompt": """You are an AI assistant specialized in OSINT (Open Source Intelligence) and information gathering. Your task is to analyze the provided data and give insights based on the leaked information found. Please be factual and objective in your analysis. Do not engage in or encourage any illegal activities. Respect privacy and use information ethically.

Given the following leaked data: {}

Please provide a detailed analysis including:
1. Overview of the data leaked
2. Potential security implications
3. Recommendations for affected parties
4. General cybersecurity best practices

Format your response in a clear, professional manner."""
    }

    start_shell(darkgpt, debug=args.debug)

    if args.debug:
        print_debug("DarkGPT and ConversationalShell initialized with debug mode enabled.")

# Punto de entrada principal para ejecutar la aplicación
if __name__ == "__main__":
    main()
