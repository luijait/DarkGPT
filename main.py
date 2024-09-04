from cli import ConversationalShell
from DarkAgent import DarkGPT
from openai import OpenAIError

# Banner de inicio para la aplicación, mostrando un diseño ASCII con el creador
banner = """
________       __        _______   __   ___       _______    _______  ___________  
|"      "\\     /""\\      /"      \\ |/"| /  ")     /" _   "|  |   __ "\\("     _   ") 
(.  ___  :)   /    \\    |:        |(: |/   /     (: ( \\___)  (. |__) :))__/  \\__/  
|: \\   ) ||  /' /\\  \\   |_____/   )|    __/       \\/ \\       |:  ____/    \\_ /     
(| (___\\ || //  __'  \\   //      / (// _  \\       //  \\ ___  (|  /        |.  |     
|:       :)/   /  \\  \\ |:  __   \\ |: | \\  \\     (:   _(  _|/|__/ \\       \\:  |     
(________/(___/    \\___)|__|  \\___)(__|  \\__)     \\_______)(_______)       \\__|     

hecho por: @luijait_
fork de: lvoidi
"""
print(banner)

def main():
    try:
        darkgpt = DarkGPT()
        conversational_shell = ConversationalShell(darkgpt)
        conversational_shell.Start()
    except OpenAIError:
        print("No has definido las variables de entorno: Define OPENAI_API_KEY, GPT_MODEL_NAME, DEHASHED_API_KEY, DEHASHED_USERNAME")
        exit(1)

# Punto de entrada principal para ejecutar la aplicación
if __name__ == "__main__":
    main()

