import os
import json
import time
from dotenv import load_dotenv
from swarm import Swarm, Agent
from openai import OpenAI
from utils.dehashed import print_debug, query_dehashed
from utils.leakosint import query_leakosint
import instructor
from pydantic import BaseModel
from typing import List, Optional

class RelevantData(BaseModel):
    name: Optional[str]
    email: Optional[str]
    password: Optional[str]
    telephone: Optional[str]

class RelevantDataFormat(BaseModel):
    results: List[RelevantData]

load_dotenv()

# ANSI escape codes for colored output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"

class DarkGPT:
    def __init__(self, model_name, temperature, agent_prompt, api_choice=None, debug=False, enable_ollama=False, log=True):
        self.model_name = model_name
        self.temperature = temperature
        self.agent_prompt = agent_prompt
        self.api_choice = api_choice
        self.debug = debug
        self.log = log
        self.enable_ollama = enable_ollama
        self.openai_client = None
        self.client = self.client_init()
        self.target_api_function = query_dehashed if self.api_choice == "dehashed" else query_leakosint
       
        #Agents
        self.osint_scrapper = Agent(name="OsintScrapper",
                                 model_override=self.model_name,
                                 instructions=self.agent_prompt,
                                 functions=[self.target_api_function, self.report_leaks]
        )

        self.user_agent = Agent(name="Helper_Agent",
                                 model_override=self.model_name,
                                 instructions=open("prompts/user_cli_prompt.txt").read(),
        )

    def client_init(self):
        
        if os.getenv("ENABLE_OLLAMA") or self.enable_ollama:
            self.openai_client = OpenAI(base_url="http://localhost:8000/v1")
            print("Using Ollama API")
        elif "deepseek" in self.model_name:
            self.openai_client = OpenAI(base_url="https://api.deepseek.com/v1")
            print("Using DeepSeek API")
        else:
            self.openai_client = OpenAI()
            print("Using OpenAI API")
        client = Swarm(self.openai_client) # Init Agents

        return client
        
    def run(self, context):
        print_debug(f"{GREEN}[+] AGENT WORKING - PROCESSING YOUR REQUEST{RESET}", is_warning=True)
        leaks_from_gpt = self.client.run(model_override=self.model_name, agent=self.osint_scrapper, messages=context, debug=self.debug, max_turns=6)

        if leaks_from_gpt and leaks_from_gpt.messages:
            for message in leaks_from_gpt.messages:
                if message.get("role") == "assistant":
                    print(message["content"])


    def router(self, agent_name):
        if agent_name == "Helper_Agent":
            return self.user_agent

    def report_leaks(self, markdown_report, report_name):
        print(f"{GREEN}[+] REPORTING LEAKS{RESET}")

        print(markdown_report)
        if self.log:
            if not os.path.exists("logs"):
                os.makedirs("logs")
            with open(f"logs/{report_name}.txt", "w") as f:
                f.write(markdown_report)
        return markdown_report
