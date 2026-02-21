# https://alphacephei.com/vosk/models

import json

import vosk
import sys
import sounddevice as sd
import queue

from services.text_2_voice import Text2Voice
from services.ollama import LLMTextService, MODEL_GEMMA_3, MODEL_LLAMA3_3

q = queue.Queue()
speaker = Text2Voice()

def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

model = vosk.Model("./models/vosk-model-de-0.21")  # Replace with the path to your downloaded model

samplerate = int(sd.query_devices(None, 'input')['default_samplerate']) # Get default sample rate

rec = vosk.KaldiRecognizer(model, samplerate)
llm = LLMTextService(model=MODEL_GEMMA_3)
# FIXME: use https://huggingface.co/google/gemma-3-27b-it
# FIXME: text to speech: https://huggingface.co/HiDream-ai/HiDream-I1-Full
#   remove bitnet
# llm = Bitnet()
speaker.select_voice("com.apple.eloquence.de-DE.Grandma")

conversation = []
initial_text = llm.say("")
print("INTRO:")
print(initial_text)
print("\n\n")
speaker.say(initial_text)

with sd.RawInputStream(samplerate=samplerate, blocksize = 8000, device=None, dtype='int16',
                       channels=1, callback=callback) as stream:
    print('#' * 80)
    print('Press Ctrl+C to stop the recording')
    print('#' * 80)

    while True:
        data = q.get()
        if rec.AcceptWaveform(data):
            res = rec.Result()
            print("Recording pause")
            data = json.loads(res)
            question = str(data["text"]).strip()
            if question:
                stream.stop()
                conversation.append(question)
                print(f"Q: {question}")
                # answer = llm.say("\n".join(conversation))
                answer = llm.say(question)
                conversation.append(answer)

                print(f"A: {answer}")
                # Text sprechen
                speaker.say(answer)
                print('Recording start')
                stream.start()

        # else:
        #     res = rec.PartialResult()
        #     print(res)