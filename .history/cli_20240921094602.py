import os
from darkgpt import GPT_with_function_output, print_debug
from darkgpt import execute_function_call, process_history_with_function_output
from darkgpt import execute_function_call, process_history_with_function_output
from darkgpt import execute_function_call, process_history_with_function_output
from darkgpt import execute_function_call, process_history_with_function_output
from darkgpt import execute_function_call, process_history_with_function_output

def start_shell(darkgpt, debug=False):
    print("Welcome to DarkGPT, a reduced version of the OSINT Agent of our 0dAI model. "
          "A wizard that uses GPT-4 to do database queries and filtered information written by @luijait_. "
          "Type 'exit' to finish, 'clear' to clear the screen. "
          "If you want an improved version of this agent with autonomous pentesting and hacking functions, visit https://0dai.omegaai.io")

    try:
        while True:
            user_input = input("> ").strip()
            if user_input.lower() == 'exit':
                print("Terminated the session.")
                break
            elif user_input.lower() == 'clear':
                os.system('cls' if os.name == 'nt' else 'clear')
            else:
                process_input(darkgpt, user_input, debug)
    except KeyboardInterrupt:
        print("\nSession terminated by the user.")

def process_input(darkgpt, user_input, debug=False):
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
        debug=debug
    )
