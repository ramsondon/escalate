# https://alphacephei.com/vosk/models
import json
import queue
import sys

import sounddevice as sd
import vosk

q = queue.Queue()


def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text


def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))


model = vosk.Model("./models/vosk-model-de-0.21")  # Replace with the path to your downloaded model

samplerate = int(sd.query_devices(None, 'input')['default_samplerate'])  # Get default sample rate

rec = vosk.KaldiRecognizer(model, samplerate)

with sd.RawInputStream(samplerate=samplerate, blocksize=8000, device=None, dtype='int16',
                       channels=1, callback=callback):
    print('#' * 80)
    print('Press Ctrl+C to stop the recording')
    print('#' * 80)

    while True:
        data = q.get()
        if rec.AcceptWaveform(data):
            res = rec.Result()
            data = json.loads(res)
            print(data["text"])

        # else:
        #     res = rec.PartialResult()
        #     print(res)
