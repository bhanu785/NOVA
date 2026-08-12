import sounddevice as sd
import numpy as np
from openwakeword.model import Model
import os, time
from faster_whisper import WhisperModel
from tools import TOOLS

RATE = 16000
CHUNK = 1280
COOLDOWN_SECS = 10.0
THRESHOLD = 1160
SILENCE_THRESHOLD = 21
last_trigger_time = 0.0
wwdetect = True
talking = False
chunks = []

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
recording_file = os.path.join(project_root, "audio", "recording.wav")

model_file = os.path.join(project_root, "audio", "hey_nova.onnx")
model_key = "hey_nova"
command = ""
# llm_process = False

# initializing wakeword model
ww_model = Model(
    wakeword_models=[model_file],
    inference_framework="onnx"
)
model = WhisperModel("small", device="cpu", compute_type="int8")

# Sounddevice requires 16 kHz sample rate

print(f"Listening for '{model_key}...'")

def set_wwdetect(value: bool) -> None:
    global wwdetect
    wwdetect = value

def get_wwdetect() -> bool:
    global wwdetect
    return wwdetect

def set_talking(value: bool) -> None:
    global talking
    talking = value

def get_talking() -> bool:
    global talking
    return talking

def get_command() -> str:
    global command
    return command

# def get_llm_process() -> bool:
#     global llm_process
#     return llm_process

# def set_llm_process(value: bool) -> None:
#     global llm_process
#     llm_process = value

# function to start the audio capture and return numpy array
def ww_stream_and_transcribe():
    # global wwdetect, talking, command, llm_process
    global wwdetect, talking, command
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
                print(f"Transcribed: {transcribed}")
                chunks.clear()
                command = transcribed
                talking = False
                wwdetect = True
                # llm_process = True
                break
            time.sleep(0.1)
            

def ww_transcribe(chunk: list) -> str:
    audio = np.concatenate(chunk).astype(np.float32) / 32768.0 
    segments, info = model.transcribe(audio, language="en", beam_size=3)
    for segment in segments:
        return segment.text
