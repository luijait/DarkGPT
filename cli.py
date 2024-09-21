import os
from darkgpt import GPT_with_function_output, print_debug

def start_shell(darkgpt, api_choice, debug=False):
    print(f"Welcome to DarkGPT, the best OSINT Agent "
          f"A wizard that uses GPT-4 to do database queries and filtered information written by @luijait_. "
          f"Type 'exit' to finish, 'clear' to clear the screen. "
          f"Using {api_choice.upper()} API. "
          f"Twitter @luijait_")

    try:
        while True:
            user_input = input("> ").strip()
            if user_input.lower() == 'exit':
                print("Terminated the session.")
                break
            elif user_input.lower() == 'clear':
                os.system('cls' if os.name == 'nt' else 'clear')
            else:
                process_input(darkgpt, user_input, api_choice, debug)
    except KeyboardInterrupt:
        print("\nSession terminated by the user.")

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
