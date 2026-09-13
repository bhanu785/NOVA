from tools import TOOLS
from listen import listen
from llm import llm_process
from openwakeword.model import Model

# dictionary of all tools
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

# main loop, listens for command and sends to llm for processing, then executes the tools returned by llm
while True:
    try:
        command = listen()
        # had to add this tts returned thank you sometimes and was messing with the loop
        if command == "Thank you":
            continue
        elif command:
            print(f"Command received: {command}")
            response = llm_process(command)
            print(response)
            for tool in response:
                tool_name = tool.function.name
                tool_args = tool.function.arguments
                tools[tool_name](**tool_args)
    except KeyboardInterrupt:
        print("Stopping...")
        break