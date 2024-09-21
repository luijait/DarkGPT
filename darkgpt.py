import os
import json
import time
from dotenv import load_dotenv
from openai import Client
from utils import print_debug
from leaks_api import query_dehashed, query_leakosint
from functions import Leak_Function
import instructor
from pydantic import BaseModel
from typing import List, Optional

load_dotenv()

# ANSI escape codes for colored output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"

def execute_function_call(openai_client, model_name, functions, message, api_choice, debug=False):
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
        if api_choice == "dehashed":
            processed_output = query_dehashed(preprocessed_output.get('queries', []), debug=debug)
        elif api_choice == "leakosint":
            processed_output = query_leakosint(preprocessed_output.get('queries', []), debug=debug)
        if debug:
            print_debug(f"Processed output from {api_choice.capitalize()} API: {processed_output}")
    except Exception as e:
        if debug:
            print_debug(f"Error during {api_choice.capitalize()} API consultation: {e}", is_error=True)
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

class DehashedResult(BaseModel):
    name: Optional[str]
    email: Optional[str]
    password: Optional[str]
    telephone: Optional[str]

class DehashedResponse(BaseModel):
    results: List[DehashedResult]

# Enable response_model in OpenAI client
client = instructor.patch(Client())

def GPT_with_function_output(openai_client, model_name, temperature, functions, agent_prompt, historial, callback=None, api_choice=None, debug=False):
    if debug:
        print_debug(f"Starting GPT_with_function_output with historial: {historial}")

    message = historial[-1].get("USUARIO", "")
    function_output = execute_function_call(openai_client, model_name, functions, message, api_choice, debug=debug)

    if debug:
        print_debug(f"Function output: {function_output}")

    historial_json = process_history_with_function_output(agent_prompt, historial, function_output, debug=debug)

    if debug:
        print_debug(f"History JSON for OpenAI API: {historial_json}")

    try:
        if api_choice == "dehashed" or api_choice == "leakosint":
            response = openai_client.chat.completions.create(
                model=model_name,
                temperature=temperature,
                messages=historial_json,
                response_model=DehashedResponse,
                max_retries=2
            )
            if debug:
                print_debug(f"Structured Dehashed response: {response}")
            
            # Convert structured response to string for streaming
            streamed_response = response.model_dump_json(indent=2)
        else:
            response = openai_client.chat.completions.create(
                model=model_name,
                temperature=temperature,
                messages=historial_json,
                stream=True
            )
            if debug:
                print_debug("OpenAI API streaming started.")
            
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
    except Exception as e:
        if debug:
            print_debug(f"Error during OpenAI API call: {e}", is_error=True)
        return

    if debug:
        print_debug(f"Final Response: {streamed_response}")

