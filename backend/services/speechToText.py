import numpy as np
import sounddevice as sd
import time
import json
from pathlib import Path
from services.setup_io_devices import resolve_input_device_index

# #region agent log
def _dbg_stt(hypothesis_id, location, message, data=None):
    try:
        log_path = Path(__file__).resolve().parents[2] / "debug-8c9fdb.log"
        payload = {"sessionId": "8c9fdb", "hypothesisId": hypothesis_id, "location": location, "message": message, "data": data or {}, "timestamp": int(time.time() * 1000)}
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(payload) + "\n")
    except Exception:
        pass
# #endregion


# transcribe audio to text using the Whisper model
def speech_to_text(model, audio, sample_rate):
    # flatten from (samples, 1) → (samples,)
    audio = np.squeeze(audio)

    # transcribe the audio using the Whisper model
    segments, info = model.transcribe(audio, beam_size=1)
    text = ""
    for segment in segments:
        text += segment.text + " "

    return text.strip()

def record_audio_vad(
    sample_rate=16000,
    silence_limit=1.2,   # seconds of silence before stop
    chunk_duration=0.3,   # how often we check audio
    mic_index=None
):
    mic_index = resolve_input_device_index(mic_index)
    # #region agent log
    _dbg_stt("B", "speechToText.py:record_audio_vad", "resolved mic index", {"mic_index": mic_index})
    # #endregion
    if mic_index is None:
        raise RuntimeError("No input microphone device available")

    audio_buffer = []
    silence_start = None

    def callback(indata, frames, time_info, status):
        nonlocal audio_buffer, silence_start

        audio = indata[:, 0]
        audio_buffer.append(audio.copy())

        # volume detection (RMS)
        volume = np.sqrt(np.mean(audio ** 2))

        if volume < 0.01:  # silence threshold (tune this)
            if silence_start is None:
                silence_start = time.time()
        else:
            silence_start = None

    with sd.InputStream(
        device=mic_index,
        samplerate=sample_rate,
        channels=1,
        callback=callback,
        blocksize=int(sample_rate * chunk_duration)
    ):
        while True:
            time.sleep(0.1)

            if silence_start is not None:
                if time.time() - silence_start > silence_limit:
                    print("Silence detected, stopping recording...")
                    break

    audio = np.concatenate(audio_buffer, axis=0)

    return audio, sample_rate

# Example usage
if __name__ == "__main__":
    audio, sr = record_audio_vad()
    text = speech_to_text(audio, sr)

    print("Transcribed text:", text)