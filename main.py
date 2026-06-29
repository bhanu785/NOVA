from tools import open_app, close_app, speak
from listen import transcribe
from brain import llm_process
import json


command = transcribe("recording.wav")
print(command)

result = llm_process(command)
print(result)
data = json.loads(result)

if data["action"] == "open":
    speak(data["speech"])
    open_app(data["app"])
elif data["action"] == "close":
    speak(data["speech"])
    close_app(data["app"])
else:
    print("couldn't find app")
