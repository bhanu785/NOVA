import subprocess, time, webbrowser, wave
import pyautogui as pag
from piper import PiperVoice
import sounddevice as sd
import soundfile as sf
from AppKit import NSWorkspace
# from Quartz import CGWindowListCopyWindowInfo, kCGWindowListOptionOnScreenOnly, kCGNullWindowID
from py2mac.application import get_running_applications, Application
import psutil


def open_app(app: str) -> None:
    subprocess.Popen(["open", "-a", app])
    time.sleep(3)
    pag.hotkey("ctrl", "command", "f")

def close_app(app: str) -> None:
    subprocess.Popen(["killall", app])

def search_browser(query: str) -> None:
    webbrowser.open(query)

def speak(text: str) -> None:
    voice = PiperVoice.load("/Users/bhanukoushikmakkapati/Desktop/NOVA/audio/en_US-ryan-medium.onnx")
    with wave.open("audio/test.wav", "wb") as wav_file:
        voice.synthesize_wav(text, wav_file)
    data, fs = sf.read("audio/test.wav")
    sd.play(data, fs)
    sd.wait()
    
def open_window() -> None:
    # running_apps = NSWorkspace.sharedWorkspace().runningApplications()

    # app_names = [app.localizedName() for app in running_apps]
    # print("Open Applications:")
    # for name in sorted(set(app_names)):
    #     print(f"- {name}")
    print("All Open Processes and Apps:")
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            print(f"PID: {proc.info['pid']} | Name: {proc.info['name']}")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

def type(text: str, duration: float) -> None:
    time.sleep(5) # only for enough time to switch tabs for testing take out later (or not)
    pag.write(text, interval=duration)

def get_open_apps() -> None:
    apps = get_running_applications()
    for app in apps:
        print(app.localized_name, app.pid)

def use_shortcut(*args: str) -> None:
    hotkeys = list(args)

    for x in hotkeys:
        pag.keyDown(x)
        time.sleep(0.05)

    for y in reversed(hotkeys):
        pag.keyUp(y)