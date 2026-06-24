
import requests
from config.prompts import PERSONALITIES, MODEL_MAP

OLLAMA_URL = "http://localhost:11434/api/generate"

current_personality = "default"

def ask_model(prompt, task="general"):

    #  Setup the model based on the task, default to "llama3" for general
    model = MODEL_MAP.get(task, "llama3")
    system_prompt = PERSONALITIES.get(current_personality, PERSONALITIES["default"])
    full_prompt = system_prompt + "\nUser: " + prompt

    # Send the prompt to the Ollama API
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": model,
            "prompt": full_prompt,
            "stream": False,
            "options": {
                "num_predict": 150 # Controls response lenght.
            }
        }
    )

    # return the response text
    return response.json()["response"]
