import pyaudio
import wave
import threading
import sounddevice as sd
import soundfile as sf

class Recorder():

    def __init__(self):
        self.audio = pyaudio.PyAudio()

        # STATES
        self.RECORDING  = False
        self.DIRECT_MONITORING = False
        self.PLAY_WHILE_RECORD = False

        # AUDIO OPTIONS
        self.BIT_RATE = pyaudio.paInt16
        self.SAMPLING_RATE = 44100
        self.CHUNK_SIZE = 1024
        self.CHANNELS = 1


        # Audio Setup
        self.stream_in = self.audio.open(format=self.BIT_RATE, channels=self.CHANNELS, rate=self.SAMPLING_RATE, input=True, frames_per_buffer=self.CHUNK_SIZE)
        self.stream_out1 = self.audio.open(format=self.BIT_RATE, channels=self.CHANNELS, rate=self.SAMPLING_RATE, output=True, frames_per_buffer=self.CHUNK_SIZE)
        self.stream_out2 = self.audio.open(format=self.BIT_RATE, channels=self.CHANNELS, rate=self.SAMPLING_RATE, output=True, frames_per_buffer=self.CHUNK_SIZE)
        self.frames = []
        self.tracks = []
        self.tracknumber = 0

    def start_recording(self):

        # RESET
        self.frames = []
        self.RECORDING = True

        # RELOAD STREAMS
        if self.DIRECT_MONITORING or self.PLAY_WHILE_RECORD:
            self.stream_out1 = self.audio.open(format=self.BIT_RATE, channels=self.CHANNELS, rate=self.SAMPLING_RATE, output=True,
                                     frames_per_buffer=self.CHUNK_SIZE)
            self.stream_out2 = self.audio.open(format=self.BIT_RATE, channels=self.CHANNELS, rate=self.SAMPLING_RATE, output=True,
                                     frames_per_buffer=self.CHUNK_SIZE)

        # RECORD NEW TRACK
        while self.RECORDING:
            try:

                # MICROPHONE INPUT
                data = self.stream_in.read(self.CHUNK_SIZE, exception_on_overflow=False)
                self.frames.append(data)

                # DIRECT MONITORING ?
                if self.DIRECT_MONITORING:
                    self.stream_out1.write(data)

                # PLAY PREVIOUSLY RECORDED TRACKS?
                if len(self.tracks) > 0 and PLAY_WHILE_RECORD:
                    try:
                        self.stream_out2.write(bytes(self.tracks[0][self.frame]))
                        self.frame += 1
                    except:
                        print("Done playing old track")
                        PLAY_WHILE_RECORD = False

            except Exception as e:
                print("ERROR DURING RECORDING" + str(e))

        # SAVE TRACK AS WAV
        self.tracknumber = str(len(self.tracks))
        self.stream_in.stop_stream()
        self.stream_in.close()
        self.stream_out1.stop_stream()
        self.stream_out2.stop_stream()
        self.stream_out1.close()
        self.stream_out2.close()
        self.audio.terminate()
        sound_file = wave.open("track" + str(self.tracknumber) + ".wav", "wb")
        sound_file.setnchannels(self.CHANNELS)
        sound_file.setsampwidth(self.audio.get_sample_size(self.BIT_RATE))
        sound_file.setframerate(self.SAMPLING_RATE)
        sound_file.writeframes(b''.join(self.frames))
        sound_file.close()
        self.tracks.append(self.frames)
        print("Saved track: " + "track" + str(self.tracknumber) + ".wav")

    def stop_recording(self):
        self.RECORDING = False

    def play_track(self):
        """ TODO: Threading play"""
        if not self.RECORDING:
            print("[RECORDER] Play track" + str(self.tracknumber) + ".wav")
            filename = "track" + str(self.tracknumber) + ".wav"
            data, fs = sf.read(filename, dtype='float32')
            sd.play(data, fs)

            #status = sd.wait()  # Wait until file is done playing

    def pause_track(self):
        sd.stop()
