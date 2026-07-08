from tools import open_app, close_app, speak
from listen import transcribe
from llm import llm_process
import json

TOOLS = ["open_app", "close_app", "search_browser", "speak", "type", "use_shortcut"] # pass into llm function
command = transcribe("audio/recording.wav")
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
