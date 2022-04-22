from pedalboard import (
    Pedalboard, Convolution, Compressor, Chorus,
    Gain, Reverb, Limiter, LadderFilter, Phaser,
)
import soundfile as sf
from pydub import AudioSegment, effects
from scipy.io import wavfile
import noisereduce as nr


class WaveFile:
    """ EXAMPLE USAGE:

    track = WaveFile("test.wav")                    # open wave file test.wav
    track.add_reverb(0.3)                           # reverb with room size 30%
    track.compress(threshold_db=-12, ratio=3)       # compress audio with threshold -12dB and ratio 3
    track.add_chorus()                              # add chorus effect
    track.gain(-5)                                  # reduce gain by -5dB
    track.phaser()                                  # add phaser effect
    track.save("mixed.wav")                         # export file to a new file

    """

    def __init__(self, filename):
        self.audio, self.sample_rate = sf.read(filename)
        self.filename = filename[:-4] + ".wav"
        self.board = Pedalboard([
            # Compressor(threshold_db=-10, ratio=2),
            # Gain(gain_db=10),
            # Chorus(),
            # LadderFilter(mode=LadderFilter.Mode.HPF12, cutoff_hz=900),
            # Phaser(),
            # Convolution("./guitar_amp.wav", 1.0),
            # Reverb(room_size=0.25),
        ], sample_rate=self.sample_rate)

    def equalize(self, start=20, end=20000, resonance=0.75):
        """TODO: add correct implementation """
        self.board = Pedalboard([], sample_rate=self.sample_rate)               # reset pedal
        self.board.append(LadderFilter(mode=LadderFilter.HPF12, cutoff_hz=5000, resonance=0.75),)   # add effect
        effected = self.board(self.audio)                                       # apply pedal to wave
        with sf.SoundFile(self.filename, 'w', samplerate=self.sample_rate,channels=len(effected.shape)) as f:
            f.write(effected)

    def compress(self, threshold_db=-12, ratio=3):
        """ Compresses your audio."""
        self.board = Pedalboard([], sample_rate=self.sample_rate)               # reset pedal
        self.board.append(Compressor(threshold_db=threshold_db, ratio=ratio))   # add effect
        effected = self.board(self.audio)                                       # apply pedal to wave
        with sf.SoundFile(self.filename, 'w', samplerate=self.sample_rate,channels=len(effected.shape)) as f:
            f.write(effected)


    def add_reverb(self, room_size=0.25, wet_level=0.1, dry_level=0.1):
        """ Adds reverb to wavefile """
        self.board = Pedalboard([], sample_rate=self.sample_rate)       # reset pedal
        self.board.append(Reverb(room_size=room_size,wet_level=wet_level, dry_level=dry_level))                # add effect
        effected = self.board(self.audio)                               # apply pedal to wave
        with sf.SoundFile(self.filename, 'w', samplerate=self.sample_rate,channels=len(effected.shape)) as f:
            f.write(effected)


    def add_chorus(self):
        self.board = Pedalboard([], sample_rate=self.sample_rate)       # reset pedal
        self.board.append(Chorus())                                     # add effect
        effected = self.board(self.audio)                               # apply pedal to wave
        with sf.SoundFile(self.filename, 'w', samplerate=self.sample_rate,channels=len(effected.shape)) as f:
            f.write(effected)


    def limiter(self):
        self.board = Pedalboard([], sample_rate=self.sample_rate)       # reset pedal
        self.board.append(Limiter())                                    # add effect
        effected = self.board(self.audio)                               # apply pedal to wave
        with sf.SoundFile(self.filename, 'w', samplerate=self.sample_rate,channels=len(effected.shape)) as f:
            f.write(effected)


    def phaser(self):
        self.board = Pedalboard([], sample_rate=self.sample_rate)       # reset pedal
        self.board.append(Phaser())                                     # add effect
        effected = self.board(self.audio)                               # apply pedal to wave
        with sf.SoundFile(self.filename, 'w', samplerate=self.sample_rate,channels=len(effected.shape)) as f:
            f.write(effected)


    def gain(self, dB):
        self.board = Pedalboard([], sample_rate=self.sample_rate)       # reset pedal
        self.board.append(Gain(gain_db=dB))                             # add effect
        effected = self.board(self.audio)                               # apply pedal to wave
        with sf.SoundFile(self.filename, 'w', samplerate=self.sample_rate,channels=len(effected.shape)) as f:
            f.write(effected)

    def normalize(self, max_amplitude = -2):
        def match_target_amplitude(sound, target_dBFS):
            change_in_dBFS = target_dBFS - sound.dBFS
            return sound.apply_gain(change_in_dBFS)

        sound = AudioSegment.from_file(self.filename, "wav")
        normalized_sound = match_target_amplitude(sound, max_amplitude)
        normalized_sound.export(self.filename, format="wav")
        print("[NORMALIZER] Normalized ", self.filename, " with ", max_amplitude, " Db")


    def noise_filter(self, reduction=0.2):
        rate, data = wavfile.read(self.filename)
        reduced_noise = nr.reduce_noise(y=data, sr=rate, prop_decrease=reduction) # 20% reduction
        wavfile.write(self.filename,rate=rate, data=reduced_noise)


    def mix(self, file2):
        """ Combines two waves into one
            Mix/Merge will overwrite file """
        sound1 = AudioSegment.from_file(self.filename)
        sound2 = AudioSegment.from_file(file2)
        combined = sound1.overlay(sound2)
        combined.export(self.filename, format='wav')


    def save(self, filename):
        tmp_copy = AudioSegment.from_file(self.filename)
        tmp_copy.export(filename, format="wav")
