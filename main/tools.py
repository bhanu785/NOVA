import subprocess, time, webbrowser, wave
import pyautogui as pag
from piper import PiperVoice
import sounddevice as sd
import soundfile as sf
from AppKit import NSWorkspace, NSApplicationActivationPolicyRegular
from pathlib import Path

class TOOLS:
    def open_app(app: str) -> None:
        subprocess.Popen(["open", "-a", app])

    def close_app(app: str) -> None:
        subprocess.Popen(["killall", app])

    # def search_browser(query: str) -> None:
    #     webbrowser.open(query)

    def speak(text: str) -> None:
        voice = PiperVoice.load("/Users/bhanukoushikmakkapati/Desktop/NOVA/audio/en_US-ryan-medium.onnx")
        with wave.open("audio/test.wav", "wb") as wav_file:
            voice.synthesize_wav(text, wav_file)
        data, fs = sf.read("audio/test.wav")
        sd.play(data, fs)
        sd.wait()

    def type(text: str, duration: float = 0.07) -> None:
        time.sleep(3) # only for enough time to switch tabs for testing take out later (or not)
        pag.write(text, interval=duration)

    def use_shortcut(args: list) -> None:
        hotkeys = args

        for x in hotkeys:
            pag.keyDown(x)
            time.sleep(0.05)

        for y in reversed(hotkeys):
            pag.keyUp(y)

    # returns all open app names
    def get_open_apps() -> list[str]:
        workspace = NSWorkspace.sharedWorkspace()
        return [
            app.localizedName() for app in workspace.runningApplications()
            if app.activationPolicy() == NSApplicationActivationPolicyRegular
        ]

    # Uses applescript and subprocess module to return the open tab in each of the browser windws (ex: Safari, Chrome)
    def get_browser_windows(app_name: str) -> list[str]:
        if app_name == "Safari":
            script = f'''
            tell application "Safari"
                set resultList to ""
                repeat with w in windows
                    try
                        set resultList to resultList & (name of w) & " ||| " & (URL of current tab of w) & "\\n"
                    end try
                end repeat
                return resultList
            end tell
            '''
        else:
            script = f'''
            tell application "{app_name}"
                set resultList to ""
                repeat with w in windows
                    try
                        set resultList to resultList & (name of w) & " ||| " & (URL of active tab of w) & "\\n"
                    end try
                end repeat
                return resultList
            end tell
            '''
        try: 
            cmd = ['osascript', '-e', script]
            proc = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return proc.stdout.strip().split('\n')
        except subprocess.CalledProcessError as e:
            print("AppleScript failed!")
            print(e.stderr)
            return []

    # focuses app based on which windows (uses get_browser_windows) and url if its a browser; uses applescript
    def focus_app(app_name: str, url: str = " ") -> None:
        if app_name == "Safari" or "Google Chrome":
            script = f'''
            
            set targetURL to "{url}"

            tell application "{app_name}"
                activate
                set windowList to windows
                set foundTab to false
                
                repeat with win in windowList
                    set tabIndex to 1
                    repeat with t in tabs of win
                        if URL of t contains targetURL then
                            set active tab index of win to tabIndex
                            set index of win to 1
                            set foundTab to true
                            exit repeat
                        end if
                        set tabIndex to tabIndex + 1
                    end repeat
                    if foundTab then exit repeat
                end repeat
            end tell
            '''
        else:
            script = f'''

            tell application "{app_name}"
                activate
            end tell
            '''

        cmd = ['osascript', '-e', script]
        subprocess.run(cmd)

    # uses all windows functions and compiles relevant info into a dictionary for easy llm reading
    def get_all_window_info() -> dict[str, str]:
        BROWSERS = ["Google Chrome", "Safari"]
        info = {}
        generic_windows = []
        open_apps = TOOLS.get_open_apps()
        
        for app in open_apps:
            if app in BROWSERS:
                windows = TOOLS.get_browser_windows(app)
                for win in windows:
                    if win and "|||" in win:
                        title, url = win.split(" ||| ", 1)
                        if url != "missing value" and title != "":
                            info[title] = url

            else:
                generic_windows.append(app)
        
        info["generic_windows"] = generic_windows

        return info

    def control_volume(desired_volume: str) -> None:
        script = f'''
        set volume output volume {desired_volume}
        '''
        
        cmd = ['osascript', '-e', script]
        subprocess.run(cmd)
    
    def make_file(name: str, contents: str) -> None:
        file_path = Path(name)
        file_path.write_text(contents)

    def change_brightness(increase: bool, times: int) -> None:
        code = 145
        if increase:
            code = 144
        script = f'''
        tell application "System Events"
	        key code {code}
        end tell
        '''
        cmd = ['osascript', '-e', script]
        for x in range(0, times+1):
            time.sleep(0.1)
            subprocess.run(cmd)
            


# helper function to create tools for llm
def create_tool(name: str, description: str, properties: dict, required: list = None) -> dict:
    return {
        "type": "function",
        "function": {
            "name": name,
            "description": description,
            "parameters": {
                "type": "object",
                "properties": properties,
                "required": required or []
            }
        }
    }