from jarvis import Jarvis
from services.wakewordDetector import WakeWordDetector
from faster_whisper import WhisperModel
from services.speechToText  import speech_to_text
from services.setup_io_devices import setupInputDevice, setupOutputDevice
from db.state_db import init_db
from db.events_db import init_events_db
from managers.state_manager import StateManager
import uvicorn
from threading import Thread
from api.server import create_app
import time
from services.event_bus import EventBus

whisper_model = WhisperModel("small", device="cuda", compute_type="float16")

def transcribe(audio, sr):
    return speech_to_text(whisper_model, audio, sr)
# def run_api(app):
#     uvicorn.run(app, host="127.0.0.1", port=8000,log_level="info")
def start_api(app):
    config = uvicorn.Config(app, host="127.0.0.1", port=8000)
    server = uvicorn.Server(config)
    return server

def main():

    # Initialize jarvis
    wake_detector = None
    input_device = setupInputDevice()
    output_device = setupOutputDevice()
    init_db()
    init_events_db()
    event_bus = EventBus()
    state_manager = StateManager(event_bus=event_bus)


    jarvis = Jarvis("jarvis",
                speech_to_text_fn=transcribe, 
                input_device=input_device, 
                output_device=output_device,
                state_manager=state_manager)
    app = create_app(state_manager, event_bus=event_bus)
    server = start_api(app)
    api_thread = Thread(target=server.run)
    # api_thread = Thread(target=run_api, args=(app,),daemon=True)
    api_thread.start()
    time.sleep(2)
    # jarvis.wake()
    # wakeword-jarvis loop
    def activate_ai_assistant():
        wake_detector.pause()
        jarvis.wake()
        wake_detector.resume()

    # Start the wake word detector
    wake_detector = WakeWordDetector(
        activation_phrase="jarvis",
        on_detect=activate_ai_assistant,
        whisper_model=whisper_model,
        device=input_device["index"]
    )

    try:
        wake_detector.start()

    # except KeyboardInterrupt:
    #     print("\nStopping wake detector...")
    #     wake_detector.stop()
    except KeyboardInterrupt:
        print("Stopping...")
        wake_detector.stop()
        server.should_exit = True
        api_thread.join()


if __name__ == "__main__":
    main()
