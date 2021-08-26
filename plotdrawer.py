# Spur anzeigen
import struct
import pyaudio
import wave
import numpy as np
import sys
import matplotlib.pyplot as plt
sound_file = wave.open("spur0.wav", "r")
raw = sound_file.readframes(-1)
raw = np.fromstring(raw, dtype='int16')

plt.title("spur0.wav")
plt.plot(raw, color="blue")
plt.ylabel("Amplitude")
plt.show()