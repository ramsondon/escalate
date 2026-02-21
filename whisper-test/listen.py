import sounddevice as sd
import numpy as np
import queue
import sys
import torch
from transformers import pipeline

SAMPLE_RATE = 16000
CHUNK_SECONDS = 5

audio_queue = queue.Queue()

def audio_callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    audio_queue.put(indata.copy())

print("Loading Whisper model...")
asr = pipeline(
    "automatic-speech-recognition",
    model="openai/whisper-small",
    device=0 if torch.cuda.is_available() else -1
)

print("Listening... (Ctrl+C to stop)")

try:
    with sd.InputStream(
            samplerate=SAMPLE_RATE,
            channels=1,
            dtype="float32",
            callback=audio_callback,
    ):
        buffer = np.empty((0, 1), dtype="float32")

        while True:
            data = audio_queue.get()
            buffer = np.concatenate((buffer, data))

            if len(buffer) >= SAMPLE_RATE * CHUNK_SECONDS:
                audio = buffer[: SAMPLE_RATE * CHUNK_SECONDS]
                buffer = buffer[SAMPLE_RATE * CHUNK_SECONDS :]

                audio = audio.squeeze()
                result = asr(audio)
                print(">>", result["text"], flush=True)

except KeyboardInterrupt:
    print("\nStopped.")
