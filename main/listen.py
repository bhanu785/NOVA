from faster_whisper import WhisperModel
import scipy.io.wavfile as wav
import sounddevice as sd
# from openwakeword.model import Model
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
recording_file = os.path.join(project_root, "audio", "recording.wav")

def listen() -> None:
    fs = 16000
    duration = 5.0
    # records from system converts into numpy array
    myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    # creates audio file using recorded audio
    wav.write(recording_file, fs, myrecording)

def transcribe(audio) -> str:
    # listen() commented for testing purposes maybe uncomment later?
    # loads audio file into faster-whisper model and returns text
    model = WhisperModel("small", device="cpu", compute_type="int8")
    segments, info = model.transcribe(audio, beam_size=3)
    for segment in segments:
        return segment.text