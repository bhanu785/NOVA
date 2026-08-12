from tools import TOOLS
# from listen import ww_stream_and_transcribe, get_wwdetect, set_wwdetect, set_talking, get_command, get_llm_process, set_llm_process
from listen import ww_stream_and_transcribe, get_wwdetect, set_wwdetect, set_talking, get_command
from llm import llm_process
import time
import os
from openwakeword.model import Model

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
recording_file = os.path.join(project_root, "audio", "recording.wav")
model_file = os.path.join(project_root, "audio", "hey_nova.onnx")
ww_model = Model(
    wakeword_models=[model_file],
    inference_framework="onnx"
)
model_key = "hey_nova"
COOLDOWN_SECS = 10.0
last_trigger_time = 0.0

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

# checks the prediction and returns accuracy
while True:
    try:
        while get_wwdetect():
            for sd_buffer in ww_stream_and_transcribe():
                prediction = ww_model.predict(sd_buffer)
                score = prediction.get(model_key, 0.0)
                if score > 0.3:
                    current_time = time.time()
                    if current_time - last_trigger_time > COOLDOWN_SECS:
                        print(f"Hey NOVA detected! Score: {score:.2f}")
                        TOOLS.speak("Yes sir!")
                        last_trigger_time = current_time
                        set_wwdetect(False)
                        set_talking(True)
                        command = get_command()
                        print(f"Command received: {command}")
                        if command:
                            break
                        # if get_llm_process():
                        #     print("Activated")
                        #     response = llm_process(get_command())
                        #     print(response)
                        #     for tool in response:
                        #         tool_name = tool.function.name
                        #         tool_args = tool.function.arguments
                        #         tools[tool_name](**tool_args)
                        # set_llm_process(False)
                    # else:
                    #     pass
        response = llm_process(command)
        print(response)
        for tool in response:
            tool_name = tool.function.name
            tool_args = tool.function.arguments
            tools[tool_name](**tool_args)
        set_wwdetect(True)
    except KeyboardInterrupt:
        print("Stopping...")
        break