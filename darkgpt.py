import os
import json
import time
from dotenv import load_dotenv
from openai import Client
from dehashed_api import query_dehashed_multiple
from functions import Leak_Function

load_dotenv()

# ANSI escape codes for colored output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"

def print_debug(message, is_error=False, is_warning=False):
    color = RED if is_error else (YELLOW if is_warning else GREEN)
    print(f"{color}[DEBUG] {message}{RESET}")

def execute_function_call(openai_client, model_name, functions, message, debug=False):
    if debug:
        print_debug(f"Executing function call with message: {message}")
        print_debug(f"Function prompts: {functions}")

    messages = [
        {"role": "system", "content": "You are a metadata router, act as a NER of mails, names, phones, domains..."},
        {"role": "user", "content": message}
    ]

    if debug:
        print_debug(f"Constructed messages for OpenAI API: {messages}")

    try:
        response = openai_client.chat.completions.create(
            model=model_name,
            temperature=0,
            messages=messages,
            functions=functions
        )
        if debug:
            print_debug(f"Received response from OpenAI API: {response}")
    except Exception as e:
        if debug:
            print_debug(f"Error during OpenAI API call: {e}", is_error=True)
        return {"error": "No encontrado"}

    try:
        args = response.choices[0].message.function_call.arguments
        preprocessed_output = json.loads(args) if args else {"error": "No encontrado"}
        if debug:
            print_debug(f"Preprocessed output: {preprocessed_output}")
            time.sleep(10)
    except Exception as e:
        if debug:
            print_debug(f"Error parsing function call arguments: {e}", is_error=True)
        preprocessed_output = {"error": "No encontrado"}

    try:
        processed_output = query_dehashed_multiple(preprocessed_output.get('queries', []), debug=debug)
        if debug:
            print_debug(f"Processed output from Dehashed API: {processed_output}")
    except Exception as e:
        if debug:
            print_debug(f"Error during Dehashed API consultation: {e}", is_error=True)
        processed_output = {"error": "No encontrado"}

    return processed_output

def process_history_with_function_output(agent_prompt, messages, function_output, debug=False):
    if debug:
        print_debug(f"Processing history with function output: {function_output}")

    history_json = []
    history_content = agent_prompt.format(json.dumps(function_output))
    history_json.append({"role": "system", "content": history_content})

    if debug:
        print_debug(f"Added system prompt to history: {history_content}")

    for message in messages:
        if "USUARIO" in message:
            history_json.append({"role": "user", "content": message["USUARIO"]})
            if debug:
                print_debug(f"Added user message to history: {message['USUARIO']}")
        elif "ASISTENTE" in message:
            history_json.append({"role": "assistant", "content": message["ASISTENTE"]})
            if debug:
                print_debug(f"Added assistant message to history: {message['ASISTENTE']}")

    if debug:
        print_debug(f"Finalized history JSON: {history_json}")

    return history_json

def GPT_with_function_output(openai_client, model_name, temperature, functions, agent_prompt, historial, callback=None, debug=False):
    if debug:
        print_debug(f"Starting GPT_with_function_output with historial: {historial}")

    message = historial[-1].get("USUARIO", "")
    function_output = execute_function_call(openai_client, model_name, functions, message, debug=debug)

    if debug:
        print_debug(f"Function output: {function_output}")

    historial_json = process_history_with_function_output(agent_prompt, historial, function_output, debug=debug)

    if debug:
        print_debug(f"History JSON for OpenAI API: {historial_json}")

    try:
        response = openai_client.chat.completions.create(
            model=model_name,
            temperature=temperature,
            messages=historial_json,
            stream=True
        )
        if debug:
            print_debug("OpenAI API streaming started.")
    except Exception as e:
        if debug:
            print_debug(f"Error during OpenAI API streaming: {e}", is_error=True)
        return

    streamed_response = ""
    for chunk in response:
        try:
            content = chunk.choices[0].delta.content or "\n"
            streamed_response += content
            print(content, end="")
            if debug:
                print_debug(f"Streamed chunk: {content}")
        except Exception as e:
            if debug:
                print_debug(f"Error processing streamed chunk: {e}", is_error=True)
            pass 
        
    if debug:
        print_debug(f"Final Response: {streamed_response}")

