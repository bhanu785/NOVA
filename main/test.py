# # This file was created for the sole purpose of testing functions from tools.py DELETE LATER
# from tools import TOOLS
import sounddevice as sd
# import numpy as np
from openwakeword.model import Model
import os, time
from listen import transcribe
import scipy.io.wavfile as wav

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
recording_file = os.path.join(project_root, "audio", "recording.wav")

model_file = os.path.join(project_root, "audio", "hey_nova.onnx")
model_key = "hey_nova"

# initializing wakeword model
model = Model(
    wakeword_models=[model_file],
    inference_framework="onnx"
)

# Sounddevice requires 16 kHz sample rate
RATE = 16000
CHUNK = 1280
last_trigger_time = 0.0
COOLDOWN_SECS = 2.0

print(f"Listening for '{model_key}...'")

# function to start the audio capture and return numpy array
def nova_stream_generator():
    global stop_check
    stop_check = False
    with sd.InputStream(samplerate=RATE, channels=1, dtype='int16', blocksize=CHUNK) as stream:
        while stop_check == False:
            audio_chunk, _ = stream.read(CHUNK)
            if stop_check == False:
                yield audio_chunk.flatten()
            else:
                stream.stop()
def cmd_record_and_transcribe(audio):
    with sd.InputStream(samplerate=RATE, channels=1, dtype='float32', blocksize=CHUNK) as raw_stream:
        while True:
            cmd_audio, _ = raw_stream.read(CHUNK)
            wav.write(audio, RATE, cmd_audio.flatten())
            text = transcribe(audio)
            if text != None:
                print(text)
# checks the prediction and returns accuracy
try:
    for sd_buffer in nova_stream_generator():
        prediction = model.predict(sd_buffer)
        score = prediction.get(model_key, 0.0)
        if score > 0.35:
            current_time = time.time()
            if current_time - last_trigger_time > COOLDOWN_SECS:
                print(f"Hey NOVA detected! Score: {score:.2f}")
                stop_check = True
                print("actually listening: ")
                cmd_record_and_transcribe(recording_file)
            else:
                pass
except KeyboardInterrupt:
    print("\nStopping...")

