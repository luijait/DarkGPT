from cli import parse_arguments, start_shell
from utils import print_debug
from darkgpt import DarkGPT
import os
from dotenv import load_dotenv
load_dotenv()

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

def main():
    args = parse_arguments()
    
    missing_keys = []
    if not os.getenv("OPENAI_API_KEY"):
        missing_keys.append("OPENAI_API_KEY")
    if not os.getenv("DEHASHED_API_KEY"):
        missing_keys.append("DEHASHED_API_KEY")
    if not os.getenv("DEHASHED_USERNAME"):
        missing_keys.append("DEHASHED_USERNAME")
    if args.api == "leakosint":
        if not os.getenv("LEAKOSINT_API_KEY"):
            missing_keys.append("LEAKOSINT_API_KEY")
    else:
        args.api = "dehashed"        

    if missing_keys:
        for key in missing_keys:
            print_debug(f"WARNING: {key} not found in environment variables.", is_warning=True)
            print_debug(f"CRITICAL: {key} is missing. The application will not function correctly without it.", is_error=True)
        print_debug("Please set the missing API keys in your .env file.", is_error=True)

    darkgpt = {
        "model_name": os.getenv("GPT_MODEL_NAME"),
        "temperature": 0.7,
        "agent_prompt": open("prompts/base_gpt_prompt.txt").read()
    }

    if args.debug:
        print_debug("DarkGPT initialized with debug mode enabled.")

    if args.shell:
        start_shell(darkgpt, api_choice=args.api, debug=args.debug)
    else:
        initial_message = args.message if args.message else input("Enter your message: ")
        user_prompt = [{
                        "role": "user", 
                        "content": initial_message
                       }]
                       
        print(args.api)
        darkgpt = DarkGPT(
            model_name=darkgpt["model_name"],
            temperature=darkgpt["temperature"],
            agent_prompt=darkgpt["agent_prompt"],
            api_choice=args.api,
            debug=args.debug
        )
        darkgpt.run(user_prompt)


# Punto de entrada principal para ejecutar la aplicación
if __name__ == "__main__":
    main()
