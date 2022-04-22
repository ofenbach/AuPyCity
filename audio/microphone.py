#!/usr/bin/env python

import threading
import wave
import audioop
import pyaudio


class Microphone:

    def __init__(self, context):
        """ Context gives mic the information if app is in recording state """
        self.context = context

        # AUDIO OPTIONS
        self.audio = pyaudio.PyAudio()
        if context.bitdepth == 16:
            self.BIT_RATE = pyaudio.paInt16     # 32 bit for better dynamic
        elif context.bitdepth == 24:
            self.BIT_RATE = pyaudio.paInt24
        else:
            self.BIT_RATE = pyaudio.paInt32
        self.SAMPLING_RATE = context.sampling          # 48.000 and 96.000 are common
        self.CHUNK_SIZE = 256               # switch to 512 if bugs
        self.CHANNELS = 1                   # mono
        self.MIC_ID = 1                     # default 1, may change this
        self.SPEAKER_ID = 0
        self.mic_volume = 0

        # Try audio settings, then fall back if it fails to standard 44100Hz/16Bit
        try:
            self.stream_in = self.audio.open(format=self.BIT_RATE, input_device_index=self.MIC_ID, channels=self.CHANNELS, rate=self.SAMPLING_RATE,
                                             input = True, frames_per_buffer=self.CHUNK_SIZE)
        except Exception as e:
            print("[MIC] AUDIO FAILED! Trying 44100/16")
            try:
                self.stream_in = self.audio.open(format=pyaudio.paInt16, input_device_index = 1,channels = 1, input = True, rate=44100, frames_per_buffer=512)
            except Exception as e:
                print(e)

        self.stream_out = self.audio.open(format=self.BIT_RATE, channels=1, rate=self.SAMPLING_RATE, output=True, frames_per_buffer=self.CHUNK_SIZE)


    def start_record(self, output_file_name):
        """ Starts a thread to ensure isolation """
        self.context.RECORDING = True
        threading.Thread(target=self.record_thread, args=(output_file_name,)).start()

    def record_thread(self, output_file_name):

        self.record_data = []
        while self.context.RECORDING:
            try:

                # MICROPHONE INPUT
                self.data = self.stream_in.read(self.CHUNK_SIZE, exception_on_overflow=False)
                self.record_data.append(self.data)
                self.mic_volume = audioop.max(self.data, 2)

                # PLAY INPUT
                if self.context.DIRECT_MONITORING:
                    self.stream_out.write(self.data)

            except Exception as e:
                print("[MIC] ERROR DURING MAIN RECORDING LOOP" + str(e))

        # RECORDING DONE, SAVE WAV
        self.sound_file = wave.open("recordings/raw/"+output_file_name, "wb")
        self.sound_file.setnchannels(self.CHANNELS)
        self.sound_file.setsampwidth(self.audio.get_sample_size(self.BIT_RATE))
        self.sound_file.setframerate(self.SAMPLING_RATE)
        self.sound_file.writeframes(b''.join(self.record_data))
        self.sound_file.close()
        print("[MIC] New recording saved as: recordings/raw/" + output_file_name)
