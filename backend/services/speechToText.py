import numpy as np
import sounddevice as sd
import time


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
    if mic_index ==None:
        print("input Mic index not provided")
        return
    

    sd.default.device = mic_index

    print("Listening... (start speaking)")

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