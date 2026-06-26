def enable_xtts_safe_load():
    import torch
    from TTS.config.shared_configs import BaseDatasetConfig
    from TTS.tts.configs.xtts_config import XttsConfig, XttsAudioConfig
    from TTS.tts.models.xtts import XttsArgs

    torch.serialization.add_safe_globals([
        BaseDatasetConfig,
        XttsConfig,
        XttsAudioConfig,
        XttsArgs
    ])

enable_xtts_safe_load()
from TTS.api import TTS

from config.config import JARVIS_VOICE_SAMPLE
import sounddevice as sd
import time
import threading

_tts = None

def get_tts():
    global _tts

    if _tts is None:
        print("Loading XTTS model...")
        # _tts = TTS(
        #     "tts_models/multilingual/multi-dataset/xtts_v2"
        # ).to("cuda") # fix to gpu later
        _tts = TTS(
        "tts_models/multilingual/multi-dataset/xtts_v2"
        ).to('cuda')
        print("XTTS loaded.")

    return _tts

def speak(text, input_wav=None, output_wav="output.wav", output_device=None):
    if not text:
        return
    tts = get_tts()
    if not input_wav:
        input_wav = "voice_samples/Jarvis/jarvis.wav"
    wav = tts.tts(
        text=text,
        speaker_wav=input_wav,
        language="en",
        split_sentences=True
    )
    play_kwargs = {"samplerate": 24000}
    if output_device is not None:
        play_kwargs["device"] = output_device

    duration_est = len(wav) / play_kwargs["samplerate"]

    sd.play(wav, **play_kwargs)
    stop_timer = threading.Timer(duration_est + 3.0, sd.stop)
    stop_timer.start()
    try:
        sd.wait()
    finally:
        stop_timer.cancel()

# speak("Hello sir, I am jarvis your personal assistant.", "voice_samples/Jarvis/jarvis.wav", "voice_samples/ProgressVideos/output.wav")