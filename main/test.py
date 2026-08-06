# # This file was created for the sole purpose of testing functions from tools.py DELETE LATER
# from tools import TOOLS
import sounddevice as sd
import numpy as np
from openwakeword.model import Model
import os, time
# import scipy.io.wavfile as wav
from faster_whisper import WhisperModel
# from tools import TOOLS

RATE = 16000
CHUNK = 1280
COOLDOWN_SECS = 2.0
THRESHOLD = 1160
SILENCE_THRESHOLD = 21
last_trigger_time = 0.0
wwdetect = True
talking = True
chunks = []

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
recording_file = os.path.join(project_root, "audio", "recording.wav")

model_file = os.path.join(project_root, "audio", "hey_nova.onnx")
model_key = "hey_nova"

# initializing wakeword model
ww_model = Model(
    wakeword_models=[model_file],
    inference_framework="onnx"
)
model = WhisperModel("small", device="cpu", compute_type="int8")

# Sounddevice requires 16 kHz sample rate

print(f"Listening for '{model_key}...'")

# function to start the audio capture and return numpy array
def ww_stream_and_transcribe():
    silence_duration = 0
    with sd.InputStream(samplerate=RATE, channels=1, dtype='int16', blocksize=CHUNK) as stream:
        while wwdetect == True:
            audio_chunk, _ = stream.read(CHUNK)
            yield audio_chunk.flatten()
            if wwdetect == False:
                break
        while talking == True:
            audio_chunk, _ = stream.read(CHUNK)
            volume = np.max(np.abs(audio_chunk))
            chunks.append(audio_chunk.flatten())
            if volume > THRESHOLD:
                silence_duration = 0
            else:
                silence_duration += 1
            if silence_duration > SILENCE_THRESHOLD:
                transcribed = ww_transcribe(chunks)
                print(transcribed)
                chunks.clear()
                break
            time.sleep(0.1)
            

def ww_transcribe(chunk: list) -> str:
    audio = np.concatenate(chunk).astype(np.float32) / 32768.0 
    segments, info = model.transcribe(audio, language="en", beam_size=3)
    for segment in segments:
        return segment.text

# checks the prediction and returns accuracy
while wwdetect == True:
    try:
        for sd_buffer in ww_stream_and_transcribe():
            prediction = ww_model.predict(sd_buffer)
            score = prediction.get(model_key, 0.0)
            if score > 0.35:
                current_time = time.time()
                if current_time - last_trigger_time > COOLDOWN_SECS:
                    print(f"Hey NOVA detected! Score: {score:.2f}")
                    # TOOLS.speak("Listening")
                    wwdetect = False
                else:
                    pass
    except KeyboardInterrupt:
        print("\nStopping...")

