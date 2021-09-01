import pyaudio
import sounddevice as sd
import soundfile as sf
from pydub import AudioSegment, effects
import audioop

from Track import Track


class Recorder():
    """ Handles everything regarding audio
        Gets created by ui.py   """

    def __init__(self):
        self.audio = pyaudio.PyAudio()

        # STATES
        self.RECORDING  = False
        self.DIRECT_MONITORING = False
        self.PLAY_WHILE_RECORD = False
        self.NORMALIZE = False

        # AUDIO OPTIONS
        self.BIT_RATE = pyaudio.paInt16     # 32 bit for better dynamic
        self.SAMPLING_RATE = 44100          # 48.000 and 96.000 are common
        self.CHUNK_SIZE = 8096              # switch to 512 if bugs
        self.CHANNELS = 1                   # mono

        # Audio Setup
        self.stream_in = self.audio.open(format=self.BIT_RATE, channels=self.CHANNELS, rate=self.SAMPLING_RATE, input=True, frames_per_buffer=self.CHUNK_SIZE)
        self.stream_out1 = self.audio.open(format=self.BIT_RATE, channels=self.CHANNELS, rate=self.SAMPLING_RATE, output=True, frames_per_buffer=self.CHUNK_SIZE)
        self.stream_out2 = self.audio.open(format=self.BIT_RATE, channels=self.CHANNELS, rate=self.SAMPLING_RATE, output=True, frames_per_buffer=self.CHUNK_SIZE)
        self.tracks = []
        self.mic_volume = 0


    def start(self):


        while True:     # Keep listening to mic

            if self.RECORDING:  # RECORDING TRIGGER

                # RESET
                self.audio = pyaudio.PyAudio()
                self.stream_in = self.audio.open(format=self.BIT_RATE, channels=self.CHANNELS, rate=self.SAMPLING_RATE,
                                                 input=True, frames_per_buffer=self.CHUNK_SIZE)
                self.frame = 0
                new_track = Track("track" + str(len(self.tracks)) + ".wav", self.audio, self.BIT_RATE,self.SAMPLING_RATE, self.CHANNELS)

                # RELOAD STREAMS
                if self.DIRECT_MONITORING or self.PLAY_WHILE_RECORD:
                    self.stream_out1 = self.audio.open(format=self.BIT_RATE, channels=self.CHANNELS,
                                                       rate=self.SAMPLING_RATE, output=True,
                                                       frames_per_buffer=self.CHUNK_SIZE)
                    self.stream_out2 = self.audio.open(format=self.BIT_RATE, channels=self.CHANNELS,
                                                       rate=self.SAMPLING_RATE, output=True,
                                                       frames_per_buffer=self.CHUNK_SIZE)

                # RECORD NEW TRACK
                while self.RECORDING:
                    try:

                        # MICROPHONE INPUT
                        data = self.stream_in.read(self.CHUNK_SIZE, exception_on_overflow=False)
                        new_track.add_data(data)
                        # get mic volume
                        self.mic_volume = audioop.max(data, 2)

                        """if self.DIRECT_MONITORING:
                            self.stream_out1.write(data)

                        # PLAY PREVIOUSLY RECORDED TRACKS?
                        if len(self.tracks) > 0 and self.PLAY_WHILE_RECORD:
                            try:
                                self.stream_out2.write(bytes(self.tracks[0][self.frame]))
                                for track in tracks:
                                write(byte(track.get_frame(self.frame))
                                self.frame += 1
                            except:
                                print("Done playing old track")
                                PLAY_WHILE_RECORD = False"""

                    except Exception as e:
                        print("[RECORDER] ERROR DURING MAIN RECORDING LOOP" + str(e))

                # RESET AUDIO
                self.stream_out1.stop_stream()
                self.stream_out2.stop_stream()
                self.stream_out1.close()
                self.stream_out2.close()

                # SAVE TRACK
                self.tracks.append(new_track)
                new_track.save_file("flac")
                print("TRACK SAVED: track" + str(len(self.tracks) - 1) + ".wav")

                # normalize if active
                if self.NORMALIZE:
                    rawsound = AudioSegment.from_file(new_track.path, "wav")
                    normalizedsound = effects.normalize(rawsound)
                    normalizedsound.export(new_track.path, format="wav")

            # get mic volume
            data = self.stream_in.read(self.CHUNK_SIZE, exception_on_overflow=False)
            self.mic_volume = audioop.max(data, 2)


    def start_recording(self):
        self.RECORDING = True


    def stop_recording(self):
        self.RECORDING = False


    def play_track(self):
        """ TODO: Threading play """
        if not self.RECORDING:
            print("[RECORDER] Play track" + str(len(self.tracks)-1) + ".wav")
            filename = "track" + str(len(self.tracks)-1) + ".wav"
            data, fs = sf.read(filename, dtype='float32')
            sd.play(data, fs)


    def pause_track(self):
        sd.stop()


    def change_bitrate(self):
        if self.BIT_RATE == pyaudio.paInt16:
            self.BIT_RATE = pyaudio.paInt32
        else:
            self.BIT_RATE = pyaudio.paInt16


    def get_bitrate(self):
        if self.BIT_RATE == pyaudio.paInt16:
            return True
        else:
            return False


    def change_sampling(self):
        if self.SAMPLING_RATE == 44100:
            self.SAMPLING_RATE = 96000
        else:
            self.SAMPLING_RATE = 44100


    def get_sampling(self):
        return self.SAMPLING_RATE


    def normalize(self):
        """ IF true it will normalize every audio already existing and every new recorded
            May change this to only new audio normalize? """
        self.NORMALIZE = not self.NORMALIZE

        # optional may remove this
        if self.NORMALIZE:
            print("NORMALIZING EVERY TRACK")
            print("EVERY NEW TRACK WILL GET NORMALIZED")
            for track in self.tracks:
                rawsound = AudioSegment.from_file(track.path, "wav")
                normalizedsound = effects.normalize(rawsound)
                normalizedsound.export(track.path, format="wav")


    # modify tracks
    def mute_track(self, track_id):
        self.tracks[track_id].mute()
        return self.tracks[track_id].MUTED
