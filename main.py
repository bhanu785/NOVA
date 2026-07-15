from tools import TOOLS
from listen import transcribe
from llm import llm_process
import time


tools = {
    "open_app": TOOLS.open_app,
    "close_app": TOOLS.close_app,
    "speak": TOOLS.speak,
    "type": TOOLS.type,
    "use_shortcut": TOOLS.use_shortcut,
    "get_all_window_info": TOOLS.get_all_window_info,
    "focus_app": TOOLS.focus_app,
    "control_volume": TOOLS.control_volume,
    "make_file": TOOLS.make_file
}

start = time.perf_counter()
command = transcribe("audio/recording.wav")
print(command)
end = time.perf_counter()
print(start - end)

llm_start = time.perf_counter()
response = llm_process(command)
llm_end = time.perf_counter()
print(response)
print(llm_start - llm_end)

for tool in response:
    tool_name = tool.function.name
    tool_args = tool.function.arguments

    tools[tool_name](**tool_args)