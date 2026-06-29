import subprocess
import pyautogui as pag
import time
import webbrowser
import wave
from piper import PiperVoice
import sounddevice as sd
import soundfile as sf


def open_app(app):
    subprocess.Popen(["open", "-a", app])
    time.sleep(2)
    pag.hotkey("ctrl", "command", "f")

def close_app(app):
    subprocess.Popen(["killall", app])

def search_browser(query):
    webbrowser.open(query)

def speak(text):
    voice = PiperVoice.load("/Users/bhanukoushikmakkapati/Desktop/NOVA/en_US-ryan-medium.onnx")
    with wave.open("test.wav", "wb") as wav_file:
        voice.synthesize_wav(text, wav_file)
    data, fs = sf.read("test.wav")
    sd.play(data, fs)
    sd.wait()
    