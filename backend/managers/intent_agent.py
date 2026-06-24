from config.prompts import INTENT_PROMPT
from brain import ask_model
import json

def classify_intent(text):
    prompt = INTENT_PROMPT.format(user_input=text)
    response = ask_model(prompt)

    try:
        return json.loads(response)

    except json.JSONDecodeError:
        print("Invalid JSON:")
        print(response)

        return {
            "intent": "general_chat",
            "args": {
                "query": text
            }
        }