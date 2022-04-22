import wave

import numpy as np
import os
import numpy as np
from scipy.io import wavfile


from pydub import AudioSegment
from scipy.io import wavfile
from scipy.signal import butter, lfilter

lowcut = 20
highcut = 20000
FRAME_RATE = 0

def cutter(filename, start, end):
    newAudio = AudioSegment.from_wav(filename)
    newAudio = newAudio[start:end]
    newAudio.export('newSong.wav', format="wav")

def amplify(filename, value):
    newAudio = AudioSegment.from_wav(filename)
    newAudio = newAudio + value
    newAudio.export(filename, format="wav")

def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a

def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y

def bandpass_filter(buffer):
    global highcut
    global lowcut
    return butter_bandpass_filter(buffer, lowcut, highcut, FRAME_RATE, order=6)

def eq(filename, startfreq, endfreq, amplitude):
    global lowcut
    global highcut
    global FRAME_RATE

    lowcut = startfreq
    highcut = endfreq
    FRAME_RATE = 96000

    samplerate, data = wavfile.read(filename)
    assert samplerate == FRAME_RATE
    filtered = np.apply_along_axis(bandpass_filter, 0, data).astype('int32')

    # amplified frequencies
    wavfile.write(filename, samplerate, filtered)
    amplify(filename, amplitude)

    # unamplified frequencies
    eq_untouched(filename, endfreq, 20000)
    newAudio = AudioSegment.from_wav(filename)
    newAudio = newAudio.low_pass_filter(startfreq)
    newAudio.export(filename[:-4] + str(20) + "hz" + str(startfreq) + "hz.wav", format="wav")

    import librosa
    import IPython as ip

    y1, sample_rate1 = librosa.load(filename[:-4] + str(startfreq) + "hz" + str(endfreq) +"hzAMP.wav", mono=True)
    y2, sample_rate2 = librosa.load(filename[:-4] + str(20) + "hz" + str(startfreq) + "hz.wav", mono=True)

    # MERGE
    librosa.display.waveplot((y1 + y2) / 2, sr=int((sample_rate1 + sample_rate2) / 2))

    # REPRODUCE
    ip.display.Audio((y1 + y2) / 2, rate=int((sample_rate1 + sample_rate2) / 2))


def eq_untouched(filename, start, end):
    global lowcut
    global highcut
    global FRAME_RATE
    lowcut = start
    highcut = end
    FRAME_RATE = 96000

    samplerate, data = wavfile.read(filename)
    assert samplerate == FRAME_RATE
    filtered = np.apply_along_axis(bandpass_filter, 0, data).astype('int32')

    # unamplified frequencies
    wavfile.write(filename[:-4] + str(start) + "hz" + str(end) + "hz.wav", samplerate, filtered)