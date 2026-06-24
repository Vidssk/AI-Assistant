import sounddevice as sd
import numpy as np
import queue
import time

class WakeWordDetector:
    def __init__(
        self,
        device=None,
        sample_rate=16000,
        activation_phrase="jarvis",
        on_detect=None,
        chunk_seconds=1,
        energy_threshold=0.0005,
        cooldown=2.0,
        whisper_model=None
    ):
        self.device = device
        self.sample_rate = sample_rate
        self.activation_phrase = activation_phrase.lower()
        self.on_detect = on_detect

        self.chunk_seconds = chunk_seconds
        self.chunk_size = int(sample_rate * chunk_seconds)

        self.energy_threshold = energy_threshold
        self.cooldown = cooldown

        self.audio_queue = queue.Queue()
        self.buffer = []

        self.last_trigger = 0

        self.active = True
        self.paused = False

        self.whisper_model = whisper_model

    def _audio_callback(self, indata, frames, time_info, status):

        audio = indata[:, 0].copy()

        self.buffer.extend(audio)

        if len(self.buffer) >= self.chunk_size:

            chunk = np.array(
                self.buffer[:self.chunk_size],
                dtype=np.float32
            )

            self.buffer = self.buffer[self.chunk_size:]

            self.audio_queue.put(chunk)

    def _process_audio(self, audio):

        now = time.time()

        if now - self.last_trigger < self.cooldown:
            return

        energy = np.sqrt(np.mean(audio ** 2))

        if energy < self.energy_threshold:
            return

        segments, _ = self.whisper_model.transcribe(
            audio,
            language="en"
        )

        text = " ".join(
            segment.text
            for segment in segments
        ).lower()

        print("Wake heard:", text)

        if self.activation_phrase in text:
            self._trigger()

    def _trigger(self):

        self.last_trigger = time.time()

        print("\n🔥 WAKE WORD DETECTED\n")

        if self.on_detect:
            self.on_detect()

    def pause(self):

        print("⏸ Wake detector paused")
        self.paused = True

    def resume(self):

        while not self.audio_queue.empty():
            self.audio_queue.get_nowait()

        self.paused = False

    def stop(self):

        self.active = False

    def start(self):

        print(
            f"Listening for '{self.activation_phrase}'..."
        )
        with sd.InputStream(
            device=self.device,
            samplerate=self.sample_rate,
            channels=1,
            dtype="float32",
            callback=self._audio_callback,
        ):
            try:
                while self.active:
                    if self.paused:
                        time.sleep(0.1)
                        continue

                    try:
                        audio = self.audio_queue.get(timeout=0.1)
                        self._process_audio(audio)

                    except queue.Empty:
                        pass

            finally:
                print("Leaving InputStream")

        # with sd.InputStream(
        #     device=self.device,
        #     samplerate=self.sample_rate,
        #     channels=1,
        #     dtype="float32",
        #     callback=self._audio_callback,
        # ):

        #     while self.active:
        #         # Jarvis is active
        #         if self.paused:
        #             time.sleep(0.1)
        #             continue

        #         try:
        #             audio = self.audio_queue.get(
        #                 timeout=0.1
        #             )

        #             self._process_audio(audio)

        #         except queue.Empty:
        #             pass

        #         finally:
        #             print("Leaving InputStream")