import os

class ConversationalShell:

    def __init__(self, darkgpt, debug=False):

        self.history = {}  # Historial de comandos del usuario.
        self.darkgpt = darkgpt  # Instancia de DarkGPT para procesamiento de GPT.
        self.debug = debug
    def Start(self):

        # Mensaje de bienvenida al usuario.
        print("Welcome to DarkGPT a reduced version of the OSINT Agent of our 0dAI model a wizard that uses GPT4 to do database queries and filtered information written by @luijait_. Type 'exit' to finish, 'clear' to clear the screen. If you want an improved version of this agent and with autonomous pentesting and hacking functions, visit https://0dai.omegaai.io")
        
        try:
            while True:
                user_input = input("> ")  # Awaits user input.
                if user_input.lower() == 'exit':
                    # Terminates the session if the user types 'exit'.
                    print("Terminated the session.")
                    break
                elif user_input.lower() == 'clear':
                    # Clears the screen if the user types 'clear'.
                    os.system('cls' if os.name == 'nt' else 'clear')
                else:
                    # Processes user input.
                    self.ProcessInput(user_input)
        except KeyboardInterrupt:
            # Handles keyboard interruption to terminate the session.
            print("\nSesión terminada por el usuario.")

    def ProcessInput(self, user_input):

        def handle_chunk(chunk_content):
            if self.debug:
                print("[DEBUG] Handling chunk content")
            print(chunk_content, end="")

        # Update history with the user's input without additional text.
        self.history.update({"USUARIO": user_input})
        historial_json = [self.history]  # Prepare history for DarkGPT.

        # Call DarkGPT to process the input and handle the output with handle_chunk.
        self.darkgpt.GPT_with_function_output(historial_json, callback=handle_chunk, debug=self.debug)

        # Optionally, maintain a list of messages if needed.
        # historial_json.append({"USUARIO": user_input})
