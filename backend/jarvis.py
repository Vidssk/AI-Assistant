from agents.chat_agent import ChatAgent
from agents.code_agent import CodeAgent

from managers.app_manager import AppManager
from managers.intent_agent import classify_intent

from services.speechToText import record_audio_vad
from services.textToSpeech import speak, get_tts

from tools.dispatcher import create_dispatcher

print("Jarvis modules loaded.")

class Jarvis:
    def __init__(self, name, speech_to_text_fn, input_device, output_device, state_manager):
        self.name = name
        print(f"Initializing {self.name}...")
        self.app_manager = AppManager()
        self.chat_agent = ChatAgent(self.name)
        self.code_agent = CodeAgent(self.name)
        self.state_manager = state_manager

        # setup Input/Output Devices
        self.input_device = input_device
        self.output_device = output_device
        
        get_tts()  # Preload TTS model
        
        # Set State Statuses
        self.active = False

        self.speech_to_text_fn = speech_to_text_fn
        self.dispatcher = create_dispatcher(
            self.app_manager, self.chat_agent, self.code_agent)
    
    def greet(self):
        return f"Hello, I am {self.name}, your personal assistant."

    def perform_task(self, task):
        return f"Performing task: {task}"
    def wake(self):
        if not self.active:
            self.state_manager.update(status="active")
            print("\n🔥 JARVIS WAKING UP\n")

            self.active = True
            self.run(voice_mode=True)

    def run(self, voice_mode=False):

        if not self.active:
            print(f"{self.name} is idle...")
            return
        print(f"{self.name} is running...")

        while self.active:

            if voice_mode:
                audio, sr = record_audio_vad(mic_index=self.input_device["index"])
                user_input = self.speech_to_text_fn(audio, sr)
                print(f"You said: {user_input}")
            else:
                user_input = input("You: ")

            classified = classify_intent(user_input)

            print("Classified:", classified)

            intent = classified["intent"]
            args = classified["args"]

            if intent == "exit_jarvis":
                self.active = False
                print("Goodbye.")
                break

            handler = self.dispatcher.get(intent)

            if handler:
                try:
                    self.state_manager.update(event=intent)
                    response = handler(args)

                    if response:
                        print(response)
                        speak(response, 
                            f"voice_samples/{self.name.title()}/{self.name}.wav",
                            f"voice_samples/{self.name.title()}/output.wav")

                except Exception as e:
                    print(f"Error executing {intent}: {e}")

            else:
                print(f"Unknown intent: {intent}")
            self.state_manager.update(status="idle",agent=None,event=None)
            self.active = False


# Example usage
if __name__ == "__main__":
    # jarvis = Jarvis("Jarvis")
    # print(jarvis.greet())
    import torch
    
    print(torch.__version__)
    print(torch.version.cuda)
    print(torch.cuda.is_available())
    print(torch.cuda.get_device_name(0))
    print(torch.cuda.get_device_capability(0))
    # jarvis.run(voice_mode=False)