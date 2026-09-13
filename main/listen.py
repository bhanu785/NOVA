import sounddevice as sd
import numpy as np
from openwakeword.model import Model
import os, time
from faster_whisper import WhisperModel
from tools import TOOLS

# constants
# Sounddevice requires 16 kHz sample rate
RATE = 16000
CHUNK = 1280
COOLDOWN_SECS = 15.0
THRESHOLD = 1160
SILENCE_THRESHOLD = 21
chunks = []

# paths to audio files and model
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
recording_file = os.path.join(project_root, "audio", "recording.wav")

model_file = os.path.join(project_root, "audio", "hey_nova.onnx")
model_key = "hey_nova"

# initializing wakeword model and stt model
ww_model = Model(
    wakeword_models=[model_file],
    inference_framework="onnx"
)
model = WhisperModel("small", device="cpu", compute_type="int8")

# starts listening for wakeword and then listens for command after ww is detected
def listen():
    # last_trigger_time = 0.0
    print(f"Listening for '{model_key}...'")
    with sd.InputStream(samplerate=RATE, channels=1, dtype='int16', blocksize=CHUNK) as stream:
        while True:
            audio_chunk, _ = stream.read(CHUNK)
            prediction = ww_model.predict(audio_chunk.flatten())
            score = prediction.get(model_key, 0.0)
            if score >= 0.5:
                print(f"Hey NOVA detected! Score: {score:.2f}")
                ww_model.reset()
                TOOLS.speak("Yes sir!")
                # returns input stream to other function
                return command_listen_transcribe(stream)

# listens for command after wakeword is detected and transcribes it
def command_listen_transcribe(stream):
    print("listening for command...")
    silence_duration = 0
    while True:
        audio_chunk, _ = stream.read(CHUNK)
        volume = np.max(np.abs(audio_chunk))
        chunks.append(audio_chunk.flatten())
        # checks to see when user is silent
        if volume > THRESHOLD:
            silence_duration = 0
        else:
            silence_duration += 1
        if silence_duration > SILENCE_THRESHOLD:
            transcribed = transcribe(chunks)
            chunks.clear()
            return transcribed

# combines audio chunks into np array and transcribes it using faster-whisper model
def transcribe(chunk: list) -> str:
    text = ""
    audio = np.concatenate(chunk).astype(np.float32) / 32768.0 
    segments, info = model.transcribe(audio, language="en", beam_size=3)
    for segment in segments:
        text += segment.text
    return text