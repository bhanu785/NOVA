# NOVA

NOVA (Neural Operations Voice Assistant) is an AI voice assistant for macOS

### Capabilities

Capable of the following:

1. Listening for wakeword
2. Continuous audio streaming
3. STT
4. Silence detection
5. LLM processing user command
6. Tool call returning and execution

### Tech Stack

1. <a href="https://github.com/dscripka/openWakeWord">openWakeWord</a> - Wake Word detection
2. <a href="https://python-sounddevice.readthedocs.io/en/0.5.3/index.html">sounddevice</a> - audio streaming
3. <a href="https://github.com/SYSTRAN/faster-whisper">faster-whisper</a> - STT
4. <a href="https://github.com/OHF-Voice/piper1-gpl/blob/main/docs/API_PYTHON.md">Piper</a> - TTS
5. <a href="https://numpy.org/doc/">numpy</a> - Silence detection and audio chunks concatenation
6. <a href="https://ollama.com/library/qwen3">Ollama qwen3:8b model</a> - LLM for command processing and tool calling
7. <a href="https://pypi.org/project/soundfile/">soundfile</a> - Reading audio files for TTS
8. <a href="https://pyautogui.readthedocs.io/en/latest/">pyautogui</a> - Automating mouse and keyboard actions
9. <a href="https://docs.python.org/3/library/pathlib.html">pathlib</a> - Making files tool
10. <a href="https://developer.apple.com/library/archive/documentation/AppleScript/Conceptual/AppleScriptLangGuide/introduction/ASLR_intro.html">applescript</a> - controlling macOS application through system commands
11. Python built-in modules
    1. os - For paths
    2. time - For testing
    3. wave - Opening audio files for TTS
    4. subprocess - Running system commands

### Pipeline

<p align="center">User says "Hey NOVA"</p> <br>
<p align="center">&darr;</p>
<p align="center">Wakeword detects and starts listening for command</p> <br>
<p align="center">&darr;</p>
<p align="center">User completes command and silence is detected; transcription begins</p> <br>
<p align="center">&darr;</p>
<p align="center">Command is transcribed and sent to LLM for processing</p> <br>
<p align="center">&darr;</p>
<p align="center">LLM determines what tools to call and returns tool name and params</p> <br>
<p align="center">&darr;</p>
<p align="center">Tools are executed and NOVA starts listening for Wakeword again</p> <br>

### What I learned
The inspiration behind NOVA was Iron Man's JARVIS.  Although it isn't as intelligent and capable as JARVIS, NOVA has taught me a lot about the concepts behind voice agents, such as TTS, STT and training voice recognition models.  It also taught me a lot about automation, as it can open and close apps and control volume and brightness to name a few.  I will continue working on this project and make it more advanced and capable than it is now.  

### Future update plans
I would like to add memory to NOVA to make it feel more personal.  I am also planning to add OCR so it can "see" my screen and help me with problems.  MCP servers would also be a great addition to NOVA, as it would allow it to connect to external tools and increase its capabilities.  


