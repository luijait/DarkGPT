# Importación de módulos necesarios
import os
from darkgpt import DarkGPT
from cli import ConversationalShell

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
"""
# Imprimir el banner para dar la bienvenida al usuario
print(banner)

# Definición de la función principal
def main():
    # Creación de una instancia de DarkGPT con modo de depuración habilitado
    darkgpt = DarkGPT(debug=True)  # Enable debug mode
    # Creación de una instancia de ConversationalShell pasando la instancia de DarkGPT con modo de depuración habilitado
    conversational_shell = ConversationalShell(darkgpt, debug=True)  # Enable debug mode
    # Inicio de la shell conversacional
    conversational_shell.Start()

# Punto de entrada principal para ejecutar la aplicación
if __name__ == "__main__":
    main()

