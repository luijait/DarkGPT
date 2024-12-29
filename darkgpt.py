import os
import json
import time
from dotenv import load_dotenv
from swarm import Swarm, Agent
from openai import OpenAI
from utils import print_debug
from leaks_api import query_dehashed, query_leakosint
import instructor
from pydantic import BaseModel
from typing import List, Optional

class DehashedResult(BaseModel):
    name: Optional[str]
    email: Optional[str]
    password: Optional[str]
    telephone: Optional[str]

class DehashedResponse(BaseModel):
    results: List[DehashedResult]

load_dotenv()

# ANSI escape codes for colored output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"

class DarkGPT:
    def __init__(self, model_name, temperature, agent_prompt, api_choice=None, debug=False):
        self.model_name = model_name
        self.temperature = temperature
        self.agent_prompt = agent_prompt
        self.api_choice = api_choice
        self.debug = debug
        self.client = self.client_init()
        self.target_api_function = query_dehashed if self.api_choice == "dehashed" else query_leakosint

    def client_init(self):
        if "deepseek" in self.model_name:
            client = OpenAI(base_url="https://api.deepseek.com/v1")
            print("Using DeepSeek API")
        else:
            client = OpenAI()
            print("Using OpenAI API")

        client = Swarm(client) # Init Agents

        return client

    def query_leaks(self, message):
        osint_scrapper = Agent(name="OsintScrapper",
                                 model_override=self.model_name,
                                 instructions=self.agent_prompt,
                                 functions=[self.target_api_function]
        )

        leaks_from_gpt = self.client.run(model_override=self.model_name, agent=osint_scrapper, messages=message, debug=self.debug)

        print(leaks_from_gpt.messages[-1]["content"])

    def run(self, context):

        leaks_from_api = self.query_leaks(context)

        try:
            if self.api_choice == "dehashed" or self.api_choice == "leakosint":
                response = self.client.beta.chat.completions.parse(
                    model=self.model_name,
                    temperature=self.temperature,
                    messages=context,
                    response_format=DehashedResponse,
                )
                if self.debug:
                    print_debug(f"Structured Dehashed response: {response}")
                event = response.choices[0].message.parsed
                
            else:
                response = self.client.beta.chat.completions.parse(
                    model=self.model_name,
                    temperature=self.temperature,
                    messages=context_json,
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
            if self.debug:
                print_debug(f"Error during OpenAI API call: {e}", is_error=True)
            return

        if debug:
            print_debug(f"Final Response: {streamed_response}")