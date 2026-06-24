from config.prompts import PERSONALITIES
from brain import ask_model

class ChatAgent:
    def __init__(self, personality="default"):
        self.personality = personality


    def handle_message(self, message):
        if not message:
            print("No message provided to ChatAgent.")
            return "No message provided."
        system_prompt = PERSONALITIES.get(self.personality, PERSONALITIES["default"])
        full_prompt = system_prompt + "\nUser: " + message
        response = ask_model(full_prompt, task="general")
        return response