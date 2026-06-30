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

import signal

import os

from services.event_bus import EventBus



whisper_model = WhisperModel("small", device="cuda", compute_type="float16")



def transcribe(audio, sr):

    return speech_to_text(whisper_model, audio, sr)



def start_api(app):

    config = uvicorn.Config(app, host="127.0.0.1", port=8000)

    server = uvicorn.Server(config)

    if hasattr(server, "install_signal_handlers"):

        server.install_signal_handlers = False

    return server



def main():



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

    api_thread = Thread(target=server.run, daemon=True)

    api_thread.start()

    time.sleep(2)



    def activate_ai_assistant():

        wake_detector.pause()

        jarvis.wake(Vmode=True)

        wake_detector.resume()



    wake_detector = WakeWordDetector(

        activation_phrase="jarvis",

        on_detect=activate_ai_assistant,

        whisper_model=whisper_model,

        device=input_device["index"]

    )



    def shutdown(signum=None, frame=None):

        print("Stopping...")

        jarvis.active = False

        wake_detector.stop()

        server.should_exit = True

        event_bus.stop()

        if signum is not None:

            raise KeyboardInterrupt



    signal.signal(signal.SIGINT, shutdown)

    signal.signal(signal.SIGTERM, shutdown)



    try:

        wake_detector.start()  # normal mode: listen for wake word

        # jarvis.wake()             # test mode: keyboard input from remote laptop

    except KeyboardInterrupt:

        pass

    finally:

        shutdown()



    api_thread.join(timeout=5)

    os._exit(0 if not api_thread.is_alive() else 1)





if __name__ == "__main__":

    main()

