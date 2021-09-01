import wave


class Track:
    """ Saves track settings
        Used by recorder.py """


    def __init__(self, file_path, audio, BIT_RATE, SAMPLING_RATE, CHANNELS):

        # STATES
        self.MUTED = False
        self.SOLO = False
        self.PAN = 0
        self.GAIN = 0
        self.path = file_path
        self.audio = audio

        # AUDIO
        self.BIT_RATE = BIT_RATE
        self.SAMPLING_RATE = SAMPLING_RATE
        self.CHANNELS = CHANNELS
        self.frames = []            # empty track


    def mute(self):
        self.MUTED = not self.MUTED


    def change_pan(self, value):
        """ Value 0: Middle
            Value -1: Left
            Value 1: Right """
        self.PAN = value


    def change_gain(self, amount):
        self.GAIN = amount


    def add_data(self, data):
        self.frames.append(data)


    def save_file(self, format):

        # always save as wav
        self.sound_file = wave.open(self.path, "wb")
        self.sound_file.setnchannels(self.CHANNELS)
        self.sound_file.setsampwidth(self.audio.get_sample_size(self.BIT_RATE))
        self.sound_file.setframerate(self.SAMPLING_RATE)
        self.sound_file.writeframes(b''.join(self.frames))
        self.sound_file.close()

        # convert if wanted to flac
        #if format == "flac":
        #    song = AudioSegment.from_wav(self.path)
        #    song.export("song.flac", format="flac")


    def get_frames(self):
        return self.frames


    def get_frame(self, index):
        return self.frames[index]


    def display_plot(self):
        """ TODO: Wave Analyser Plot """
        pass