from config.prompts import PERSONALITIES
from brain import ask_model


class CodeAgent:
    def __init__(self, personality="default"):
        self.personality = personality

    def handle_code_request(self, request):
        print(f"Handling code request: {request}")
        if not request:
            print("No code request provided.")
            return "No code request provided."
        system_prompt = PERSONALITIES.get(self.personality, PERSONALITIES["default"])
        full_prompt = system_prompt + "\nUser: " + request
        response = ask_model(full_prompt, task="code")
        print(f"Generated response: {response}")
        return response