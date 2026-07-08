from faster_whisper import WhisperModel
import scipy.io.wavfile as wav
import sounddevice as sd

def listen() -> None:
    fs = 16000
    duration = 5.0
    print("Listening: ")
    # records from system
    myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    # creates audio file using recorded audio
    wav.write("audio/recording.wav", fs, myrecording)

def transcribe(audio) -> str:
    listen()
    # loads text into faster-whisper model and returns text
    model = WhisperModel("small", device="cpu", compute_type="int8")
    segments, info = model.transcribe(audio, beam_size=5)
    for segment in segments:
        return segment.text