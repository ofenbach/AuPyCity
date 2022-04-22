import threading

import pyaudio
import sounddevice as sd
import soundfile as sf
from pydub import AudioSegment, effects
import audioop

from audio.track import Track


class Recorder:
    """ Handles everything regarding audio """

    def __init__(self):

        # STATES
        self.RECORDING = False
        self.DIRECT_MONITORING = False
        self.PLAY_WHILE_RECORD = False
        self.NORMALIZE = False

        # AUDIO OPTIONS
        self.audio = pyaudio.PyAudio()
        self.BIT_RATE = pyaudio.paInt16     # 32 bit for better dynamic
        self.SAMPLING_RATE = 48000          # 48.000 and 96.000 are common
        self.CHUNK_SIZE = 128               # switch to 512 if bugs
        self.CHANNELS = 1                   # mono
        self.MIC_ID = 1                     # default 1, may change this
        self.SPEAKER_ID = 0

        # Audio Setup
        self.stream_in = self.audio.open(format=self.BIT_RATE, input_device_index = self.MIC_ID, channels=self.CHANNELS, rate=self.SAMPLING_RATE, input=True, frames_per_buffer=self.CHUNK_SIZE)
        self.stream_out_main = self.audio.open(format=self.BIT_RATE, channels=self.CHANNELS, rate=self.SAMPLING_RATE, output=True, frames_per_buffer=self.CHUNK_SIZE)
        self.tracks = []
        self.frame = 0
        self.mic_volume = 0



    def start(self):
        """ Microphone input """

        while True:     # Keep listening to mic

            if self.RECORDING:

                # RESET
                self.stream_in = self.audio.open(format=self.BIT_RATE, input_device_index=self.MIC_ID,
                                                 channels=self.CHANNELS, rate=self.SAMPLING_RATE, input=True,
                                                 frames_per_buffer=self.CHUNK_SIZE)
                self.frame = 0
                new_track = Track("track_" + str(len(self.tracks)) + ".wav", str(len(self.tracks)), self.audio, self.BIT_RATE, self.SAMPLING_RATE, self.CHANNELS)

                # RELOAD STREAMS
                #if self.DIRECT_MONITORING or self.PLAY_WHILE_RECORD:
                #    self.stream_out0 = self.audio.open(format=self.BIT_RATE, channels=self.CHANNELS,rate=self.SAMPLING_RATE, output=True,frames_per_buffer=self.CHUNK_SIZE)

                # RECORD NEW TRACK
                while self.RECORDING:
                    try:

                        # MICROPHONE INPUT
                        data = self.stream_in.read(self.CHUNK_SIZE, exception_on_overflow=False)
                        new_track.add_data(data)
                        self.mic_volume = audioop.max(data, 2)

                        if self.DIRECT_MONITORING:
                            self.stream_out_main.write(data)

                        # PLAY PREVIOUSLY RECORDED TRACKS?
                        """if len(self.tracks) > 0 and self.PLAY_WHILE_RECORD:
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

                # SAVE TRACK
                self.tracks.append(new_track)
                new_track.save_file()

                # NORMALIZE
                if self.NORMALIZE:
                    rawsound = AudioSegment.from_file(new_track.path, "wav")
                    normalizedsound = effects.normalize(rawsound)
                    normalizedsound.export(new_track.path, format="wav")

            # MIC VOLUME
            data = self.stream_in.read(self.CHUNK_SIZE, exception_on_overflow=False)
            self.mic_volume = audioop.max(data, 2)


    def start_recording(self):
        self.RECORDING = True


    def stop_recording(self):
        self.RECORDING = False

    def play_track(self, id):
        filename = "tracks/track" + str(id) + "/track_" + str(id) + ".wav"
        data, fs = sf.read(filename, dtype='float32')
        sd.play(data, fs)

    def play_tracks(self):
        if not self.RECORDING:
            try:

                # play every non muted track simultanisly
                for track in range(0,len(self.tracks)):
                    if self.tracks[track].MUTED == False:
                        print("THREADING: PLAYING TRACK")
                        threading.Thread(target=self.play_track, args=(int(track),),).start()

            except Exception as e:
                print("ERROR Playing. No recording?")
                print(e)

    def pause_track(self):
        for track in range(len(self.tracks)):
            try:
                sd.stop()
            except:
                print("err")


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

    def get_mics(self):

        info = self.audio.get_host_api_info_by_index(0)
        numdevices = info.get('deviceCount')
        mics=[]
        for i in range(0, numdevices):
            if (self.audio.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
                mics.append(self.audio.get_device_info_by_host_api_device_index(0, i).get('name'))
        return mics

    def switch_mic(self, index):
        self.MIC_ID = index
        print("Switched mic to " + str(index))

    def get_speaker(self):

        info = self.audio.get_host_api_info_by_index(0)
        numdevices = info.get('deviceCount')
        speaker = []
        for i in range(0, numdevices):
            if (self.audio.get_device_info_by_host_api_device_index(0, i).get('maxOutputChannels')) > 0:
                speaker.append(self.audio.get_device_info_by_host_api_device_index(0, i).get('name'))
        return speaker

    def switch_speaker(self, index):
        self.SPEAKER_ID = index
        print("Switched speaker to " + str(index))

    def switch_direct_monitor(self):
        self.DIRECT_MONITORING = not self.DIRECT_MONITORING