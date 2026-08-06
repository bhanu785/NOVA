# needed another file for testing type shhi
import sounddevice as sd
import numpy as np
import time
from tools import TOOLS
# RATE = 16000
# CHUNK = 1280
# THRESHOLD = 1160 # threshold for volume detection
# try:
#     with sd.InputStream(samplerate=RATE, channels=1, dtype='int16', blocksize=CHUNK) as stream:
#         while True:
#             audio_chunk, _ = stream.read(CHUNK)
#             volume = np.max(np.abs(audio_chunk))
#             # if volume > THRESHOLD:
#             #     print(f"Sound detected with volume: {volume:.2f}")
#             print(volume)
#             time.sleep(0.1)
# except KeyboardInterrupt:
#     print("Stopped listening.")