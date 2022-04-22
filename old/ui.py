import threading
from pathlib import Path
from tkinter import Tk, Canvas, Text, Button, PhotoImage
import numpy as np

from recorder import Recorder
import time

# PATH STUFF
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")
def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


# CREATE TK WINDOW
window = Tk()
window.geometry("1440x1000")    # TODO: fix this to dynamic size
window.configure(bg="#111111")
canvas = Canvas(window, bg="#111111", height=1000, width=1440, bd=0, highlightthickness=0, relief="flat")
canvas.place(x=0, y=0)
window.resizable(False, False)


class UI:
    """ Main UI, called by main.py  """


    def __init__(self):
        """ Initialize Recorder """
        self.recorder = Recorder()
        threading.Thread(target=self.recorder.start, args="").start()
        self.load_ui()
        self.display_default_ui()


    def update_micvolumebar(self):
        """ Updates the top volume bar
        TODO: fix performance """
        #eraser = True
        while True:

            volume = self.recorder.mic_volume

            # ALTERNATIVE: draw with canvas instead of images
            # TODO: fix performance to replace images
            """eraser = not eraser

            # erase old volume drawing
            if eraser:
                canvas.create_rectangle(float(397), 53,  # + float(volume // 40),
                                        float(397 + 1000), 70, fill="#1D1D1D", outline="")

            if volume < 500:
                canvas.create_rectangle(float(397), 53,  # + float(volume // 40),
                                        float(397 + volume / 3), 70, fill="#3f3f3f", outline="")
            else:
                canvas.create_rectangle(float(397), 53,  # + float(volume // 40),
                                        float(397 + volume / 5), 70, fill="#3f3f3f", outline="")"""

            if 0 <= volume < 10:
                self.button_micvolumebar.tkraise()

                # draw new volume
                self.button_micvolumebar.place(x=397, y=53, width=119.0, height=7.0)

            elif 10 <= volume < 30:
                self.button_micvolumebar1.tkraise()
            elif 30 <= volume < 50:
                self.button_micvolumebar2.tkraise()
            elif 50 <= volume < 70:
                self.button_micvolumebar3.tkraise()
            elif 70 <= volume < 100:
                self.button_micvolumebar4.tkraise()
            elif 100 <= volume < 200:
                self.button_micvolumebar5.tkraise()
            elif 200 <= volume < 300:
                self.button_micvolumebar6.tkraise()
            elif 300 <= volume < 500:
                self.button_micvolumebar7.tkraise()
            elif 500 <= volume < 1000:
                self.button_micvolumebar8.tkraise()
            elif 1000 <= volume < 2000:
                self.button_micvolumebar9.tkraise()
            elif 2000 <= volume <= 3200:
                self.button_micvolumebar10.tkraise()
            else:
                self.button_micvolumebarmax.tkraise()

            # draw recording line
            if self.recorder.RECORDING:
                self.intervall += 1

                # end reached? reset!
                if self.intervall > 1200:
                    self.intervall = 0

                    # REDRAW empty track
                    if len(self.recorder.tracks) == 0:
                        canvas.create_rectangle(218, 139, 1440.0, 309,fill="#1D1D1D", outline="")
                        canvas.create_rectangle(218, 221, 1440.0, 223,fill="#9B7347", outline="")
                        canvas.create_rectangle(218, 133, 1440.0, 139,fill="#02ECFE", outline="")
                    elif len(self.recorder.tracks) == 1:
                        canvas.create_rectangle(218, 413-89, 1440.0, 413+89, fill="#1D1D1D", outline="")    # track1 box
                        canvas.create_rectangle(218, 413, 1440.0, 415, fill="#9B7347", outline="")          # top bar
                        canvas.create_rectangle(218, 413-89, 1440.0, 413-84, fill="#02ECFE", outline="")    # orange bar

                if len(self.recorder.tracks) == 0:
                    canvas.create_rectangle(float(217+self.intervall), max(220 - float(volume//40), 133), float(217 + self.intervall), 220, fill="#9B7347",outline="")
                    canvas.create_rectangle(float(217 + self.intervall), min(220 + float(volume//40),309),float(217 + self.intervall), 220, fill="#9B7347", outline="")
                elif len(self.recorder.tracks) == 1:
                    canvas.create_rectangle(float(217 + self.intervall), max(413 - float(volume // 40),413-89),float(217 + self.intervall), 413, fill="#9B7347", outline="")
                    canvas.create_rectangle(float(217 + self.intervall), min(413 + float(volume // 40), 413+89),float(217 + self.intervall), 413, fill="#9B7347", outline="")

            else:
                self.intervall = 0.01   # initialisation
            time.sleep(0.000001)        # TODO: fix performance, keep thread low cpu


    def load_ui(self):

        # LOAD IMAGES
        self.img_normalizer = PhotoImage(file=relative_to_assets("effects_buttons/normalizer.png"))
        self.img_normalizeractive = PhotoImage(file=relative_to_assets("effects_buttons/normalizer_active.png"))
        self.img_noisereduction = PhotoImage(file=relative_to_assets("effects_buttons/noise_reduction.png"))
        self.img_compressor = PhotoImage(file=relative_to_assets("effects_buttons/compressor.png"))
        self.img_sampling = PhotoImage(file=relative_to_assets("settings_buttons/sampling_rate.png"))
        self.img_samplingactive = PhotoImage(file=relative_to_assets("settings_buttons/sampling_rate_active.png"))
        self.img_bitrate = PhotoImage(file=relative_to_assets("settings_buttons/bitrate.png"))
        self.img_bitrateactive = PhotoImage(file=relative_to_assets("settings_buttons/bitrate_active.png"))
        self.img_stereo = PhotoImage(file=relative_to_assets("settings_buttons/stereo.png"))
        self.img_gain = PhotoImage(file=relative_to_assets("track_buttons/gain.png"))
        self.img_pan = PhotoImage(file=relative_to_assets("track_buttons/pan.png"))
        self.img_panR = PhotoImage(file=relative_to_assets("track_buttons/panR.png"))
        self.img_panL = PhotoImage(file=relative_to_assets("track_buttons/panL.png"))
        self.img_pan50R = PhotoImage(file=relative_to_assets("track_buttons/pan50R.png"))
        self.img_pan50L = PhotoImage(file=relative_to_assets("track_buttons/pan50L.png"))
        self.img_solo = PhotoImage(file=relative_to_assets("track_buttons/solo.png"))
        self.img_mute = PhotoImage(file=relative_to_assets("track_buttons/mute.png"))
        self.img_x = PhotoImage(file=relative_to_assets("track_buttons/x.png"))
        self.img_pan3 = PhotoImage(file=relative_to_assets("track_buttons/pan.png"))
        self.img_timeaxis = PhotoImage(file=relative_to_assets("time_axis.png"))
        self.img_ear = PhotoImage(file=relative_to_assets("functions_buttons/ear.png"))
        self.img_redo = PhotoImage(file=relative_to_assets("functions_buttons/redo.png"))
        self.img_play = PhotoImage(file=relative_to_assets("record_buttons/play.png"))
        self.img_pause = PhotoImage(file=relative_to_assets("record_buttons/pause.png"))
        self.img_stop = PhotoImage(file=relative_to_assets("record_buttons/stop.png"))
        self.img_record = PhotoImage(file=relative_to_assets("record_buttons/record.png"))
        self.img_recordactive = PhotoImage(file=relative_to_assets("record_buttons/record_active.png"))
        self.img_microphone = PhotoImage(file=relative_to_assets("functions_buttons/microphone.png"))
        self.img_volumebar = PhotoImage(file=relative_to_assets("functions_buttons/volume_bar.png"))
        self.img_volume0 = PhotoImage(file=relative_to_assets("microphone_bar/volume0.png"))
        self.img_volume1 = PhotoImage(file=relative_to_assets("microphone_bar/volume1.png"))
        self.img_volume2 = PhotoImage(file=relative_to_assets("microphone_bar/volume2.png"))
        self.img_volume3 = PhotoImage(file=relative_to_assets("microphone_bar/volume3.png"))
        self.img_volume4 = PhotoImage(file=relative_to_assets("microphone_bar/volume4.png"))
        self.img_volume5 = PhotoImage(file=relative_to_assets("microphone_bar/volume5.png"))
        self.img_volume6 = PhotoImage(file=relative_to_assets("microphone_bar/volume6.png"))
        self.img_volume7 = PhotoImage(file=relative_to_assets("microphone_bar/volume7.png"))
        self.img_volume8 = PhotoImage(file=relative_to_assets("microphone_bar/volume8.png"))
        self.img_volume9 = PhotoImage(file=relative_to_assets("microphone_bar/volume9.png"))
        self.img_volume10 = PhotoImage(file=relative_to_assets("microphone_bar/volume10.png"))
        self.img_volumemax = PhotoImage(file=relative_to_assets("microphone_bar/volume_max.png"))
        self.img_expand = PhotoImage(file=relative_to_assets("functions_buttons/expand.png"))
        self.img_speaker = PhotoImage(file=relative_to_assets("functions_buttons/speaker.png"))
        self.img_undo = PhotoImage(file=relative_to_assets("functions_buttons/undo.png"))
        self.img_entry = PhotoImage(file=relative_to_assets("entry_1.png"))

        # LOAD BUTTONS
        self.button_record = Button(image=self.img_record,borderwidth=0,highlightthickness=0,relief="flat",
                                      command=self.start_record)
        self.button_recordactive = Button(image=self.img_recordactive, borderwidth=0, highlightthickness=0, relief="flat",
                                    command=self.start_record)
        self.button_stop = Button(image=self.img_stop, borderwidth=0, highlightthickness=0, relief="flat",
                                  command=self.stop_recording)
        self.button_pause = Button(image=self.img_pause, borderwidth=0, highlightthickness=0, relief="flat",
                                   command=self.recorder.pause_track)
        self.button_play = Button(image=self.img_play, borderwidth=0, highlightthickness=0, relief="flat",
                                  command=lambda: self.recorder.play_tracks())
        self.button_microphone = Button(image=self.img_microphone, borderwidth=0, highlightthickness=0, relief="flat",
                                        command=lambda: print("microphone clicked"))
        self.button_micvolumebar = Button(image=self.img_volumebar,borderwidth=0,highlightthickness=0,relief="flat",
                                      command=lambda: print("micvolume clicked"))
        self.button_micvolumebar1 = Button(image=self.img_volume1, borderwidth=0, highlightthickness=0, relief="flat",
                                          command=lambda: print("micvolume clicked"))
        self.button_micvolumebar2 = Button(image=self.img_volume2, borderwidth=0, highlightthickness=0, relief="flat",
                                           command=lambda: print("micvolume clicked"))
        self.button_micvolumebar3 = Button(image=self.img_volume3, borderwidth=0, highlightthickness=0, relief="flat",
                                           command=lambda: print("micvolume clicked"))
        self.button_micvolumebar4 = Button(image=self.img_volume4, borderwidth=0, highlightthickness=0, relief="flat",
                                           command=lambda: print("micvolume clicked"))
        self.button_micvolumebar5 = Button(image=self.img_volume5, borderwidth=0, highlightthickness=0, relief="flat",
                                           command=lambda: print("micvolume clicked"))
        self.button_micvolumebar6 = Button(image=self.img_volume6, borderwidth=0, highlightthickness=0, relief="flat",
                                           command=lambda: print("micvolume clicked"))
        self.button_micvolumebar7 = Button(image=self.img_volume7, borderwidth=0, highlightthickness=0, relief="flat",
                                           command=lambda: print("micvolume clicked"))
        self.button_micvolumebar8 = Button(image=self.img_volume8, borderwidth=0, highlightthickness=0, relief="flat",
                                           command=lambda: print("micvolume clicked"))
        self.button_micvolumebar9 = Button(image=self.img_volume9, borderwidth=0, highlightthickness=0, relief="flat",
                                           command=lambda: print("micvolume clicked"))
        self.button_micvolumebar10 = Button(image=self.img_volume10, borderwidth=0, highlightthickness=0, relief="flat",
                                           command=lambda: print("micvolume clicked"))
        self.button_micvolumebarmax = Button(image=self.img_volumemax, borderwidth=0, highlightthickness=0, relief="flat",
                                            command=lambda: print("micvolume clicked"))
        self.button_speakerRvolumebar = Button(image=self.img_volumebar,borderwidth=0,highlightthickness=0,relief="flat",
                                      command=lambda: print("speakerright volume clicked"))
        self.button_speakerLvolumebar = Button(image=self.img_volumebar, borderwidth=0, highlightthickness=0,relief="flat",
                                      command=lambda: print("speakerleft volume clicked"))
        self.button_timeaxis = Button(image=self.img_timeaxis, borderwidth=0, highlightthickness=0, relief="flat",
                                      command=lambda: print("timeaxis clicked"))
        self.button_ear = Button(image=self.img_ear, borderwidth=0, highlightthickness=0, relief="flat",
                                      command=lambda: self.recorder.switch_direct_monitor())
        self.button_redo = Button(image=self.img_redo, borderwidth=0, highlightthickness=0, relief="flat",
                                      command=lambda: print("redo clicked"))
        self.button_undo = Button(image=self.img_undo, borderwidth=0, highlightthickness=0, relief="flat",
                                      command=lambda: print("undo clicked"))
        self.button_speaker = Button(image=self.img_speaker, borderwidth=0, highlightthickness=0, relief="flat",
                                      command=lambda: print("speaker clicked"))
        self.button_expand = Button(image=self.img_expand, borderwidth=0, highlightthickness=0, relief="flat",
                                    command=lambda: self.show_micselection())
        self.button_expand2 = Button(image=self.img_expand, borderwidth=0, highlightthickness=0, relief="flat",
                                     command=lambda: self.show_speakerselection())


        self.button_noise = Button(image=self.img_noisereduction, borderwidth=0, highlightthickness=0, relief="flat",
                                      command=lambda: print("noise reduction"), )
        self.button_normalizer = Button(image=self.img_normalizer, borderwidth=0, highlightthickness=0, relief="flat",
                                      command=self.normalize)
        self.button_normalizeractive = Button(image=self.img_normalizeractive, borderwidth=0, highlightthickness=0, relief="flat",
                                      command=self.normalize)
        self.button_compressor = Button(image=self.img_compressor, borderwidth=0, highlightthickness=0, relief="flat",
                                      command=lambda: print("compressor clicked"))
        self.button_stereo = Button(image=self.img_stereo, borderwidth=0, highlightthickness=0, relief="flat",
                                      command=lambda: print("stereo clicked"))
        self.button_sampling = Button(image=self.img_sampling, borderwidth=0, highlightthickness=0, relief="flat",
                                      command=self.change_samplingrate)
        self.button_samplingactive = Button(image=self.img_samplingactive, borderwidth=0, highlightthickness=0, relief="flat",
                                      command=self.change_samplingrate)
        self.button_bitrate = Button(image=self.img_bitrate, borderwidth=0, highlightthickness=0, relief="flat",
                                      command=self.change_bitrate)
        self.button_bitrateactive = Button(image=self.img_bitrateactive, borderwidth=0, highlightthickness=0, relief="flat",
                                      command=self.change_bitrate)

        self.button_pan = Button(image=self.img_pan,borderwidth=0,highlightthickness=0,relief="flat",
                                      command=lambda: self.change_pan(0))
        self.button_panR = Button(image=self.img_panR, borderwidth=0, highlightthickness=0, relief="flat",
                                 command=lambda: self.change_pan(0))
        self.button_panL = Button(image=self.img_panL, borderwidth=0, highlightthickness=0, relief="flat",
                                 command=lambda: self.change_pan(0))
        self.button_pan50R = Button(image=self.img_pan50R, borderwidth=0, highlightthickness=0, relief="flat",
                                 command=lambda: self.change_pan(0))
        self.button_pan50L = Button(image=self.img_pan50L, borderwidth=0, highlightthickness=0, relief="flat",
                                 command=lambda: self.change_pan(0))
        self.button_gain = Button(image=self.img_pan,borderwidth=0,highlightthickness=0, relief="flat",
                                      command=lambda: self.change_gain(0))
        self.button_gainR = Button(image=self.img_panR, borderwidth=0, highlightthickness=0, relief="flat",
                                  command=lambda: self.change_gain(0))
        self.button_gainL = Button(image=self.img_panL, borderwidth=0, highlightthickness=0, relief="flat",
                                  command=lambda: self.change_gain(0))
        self.button_gain50R = Button(image=self.img_pan50R, borderwidth=0, highlightthickness=0, relief="flat",
                                  command=lambda: self.change_gain(0))
        self.button_gain50L = Button(image=self.img_pan50L, borderwidth=0, highlightthickness=0, relief="flat",
                                  command=lambda: self.change_gain(0))
        self.button_solo = Button(image=self.img_solo,borderwidth=0,highlightthickness=0,relief="flat",
                                      command=self.solotrack0)
        self.button_mute = Button(image=self.img_mute,borderwidth=0,highlightthickness=0,relief="flat",
                                      command=self.mute_track0)
        self.button_x = Button(image=self.img_x,borderwidth=0,highlightthickness=0,relief="flat",
                                      command=self.delete_track0)
        self.button_pan1 = Button(image=self.img_pan,borderwidth=0,highlightthickness=0,relief="flat",
                                      command=lambda: self.change_pan(1))
        self.button_pan1L = Button(image=self.img_panL, borderwidth=0, highlightthickness=0, relief="flat",
                                  command=lambda: self.change_pan(1))
        self.button_pan1_50L = Button(image=self.img_pan50L, borderwidth=0, highlightthickness=0, relief="flat",
                                  command=lambda: self.change_pan(1))
        self.button_pan1_50R = Button(image=self.img_pan50R, borderwidth=0, highlightthickness=0, relief="flat",
                                  command=lambda: self.change_pan(1))
        self.button_pan1R = Button(image=self.img_panR, borderwidth=0, highlightthickness=0, relief="flat",
                                  command=lambda: self.change_pan(1))
        self.button_gain1 = Button(image=self.img_pan,borderwidth=0,highlightthickness=0, relief="flat",
                                      command=lambda: self.change_gain(1))
        self.button_gain1R = Button(image=self.img_panR, borderwidth=0, highlightthickness=0, relief="flat",
                                  command=lambda: self.change_gain(1))
        self.button_gain1L = Button(image=self.img_panL, borderwidth=0, highlightthickness=0, relief="flat",
                                  command=lambda: self.change_gain(1))
        self.button_gain1_50R = Button(image=self.img_pan50R, borderwidth=0, highlightthickness=0, relief="flat",
                                       command=lambda: self.change_gain(1))
        self.button_gain1_50L = Button(image=self.img_pan50L, borderwidth=0, highlightthickness=0, relief="flat",
                                  command=lambda: self.change_gain(1))
        self.button_solo1 = Button(image=self.img_solo,borderwidth=0,highlightthickness=0,relief="flat",
                                      command=lambda: print("solo1 clicked"))
        self.button_mute1 = Button(image=self.img_mute,borderwidth=0,highlightthickness=0,relief="flat",
                                      command=self.mute_track1)
        self.button_x1 = Button(image=self.img_x,borderwidth=0,highlightthickness=0,relief="flat",
                                      command=lambda: print("trackx1 clicked"))

        threading.Thread(target=self.update_micvolumebar).start()   # ui real time updates


    def display_default_ui(self):
        """ Loads standard AuPyCity """

        print("[UI] DISPLAYING DEFAULT UI")

        # BOTTOM SETTINGS BOX
        canvas.create_rectangle(1.1368683772161603e-13,917.0,1440.0,1000.0,fill="#1D1D1D",outline="")

        # BOTTOM SETTINGS TEXTAREA
        canvas.create_rectangle(1278.0, 945.0, 1418.0, 974.0, fill="#1D1D1D", outline="")

        # BOTTOM SETTINGS TEXTAREA BOX
        entry_bg_1 = canvas.create_image(1306.0,959.5, image=self.img_entry)
        # text inside textarea
        entry_1 = Text(bd=0, bg="#393939", highlightthickness=0)
        entry_1.place(x=1238.0, y=945.0, width=136.0, height=27.0)

        # BOTTOM SETTINGS NOISE REDUCTION
        self.button_noise.place(x=779, y=928.0, width=73.0, height=60.0)

        # NORMALIZER
        self.button_normalizer.place(x=694, y=928.0, width=52.0, height=60.0)
        self.button_normalizeractive.place(x=694, y=928.0, width=52.0, height=60.0)
        self.button_normalizeractive.lower(self.button_normalizer)

        # COMPRESSOR
        self.button_compressor.place(x=595, y=928.0, width=57.0, height=60.0)

        # STEREO
        self.button_stereo.place(x=199, y=929.0, width=59.0, height=59.0)

        # SAMPLING RATE
        self.button_sampling.place(x=108, y=929.0, width=60.0, height=59.0)
        self.button_samplingactive.place(x=108, y=929.0, width=60.0, height=59.0)
        self.button_samplingactive.lower(self.button_sampling)

        # BITDEPTH
        self.button_bitrate.place(x=29, y=927.0, width=47.0, height=59.0)
        self.button_bitrateactive.place(x=29, y=927.0, width=47.0, height=59.0)
        self.button_bitrateactive.lower(self.button_bitrate)

        ### TOP BAR ###
        # TIME AXIS
        self.button_timeaxis.place(x=218, y=95, width=1280, height=22)

        # TIME TEXT TODO: BOX
        canvas.create_text(66, 99, anchor="nw", text="00:00:00.000", fill="#FFFFFF", font=("Roboto", 12 * -1))

        # TOP BAR FUNCTIONS BOX
        canvas.create_rectangle(0.0,23,1440,95,fill="#1D1D1D",outline="")

        # EAR DIRECT MONITORING
        self.button_ear.place(x=911, y=63, width=18.0, height=18.0)

        # REDO
        self.button_redo.place(x=935, y=37, width=18.0, height=18.0)

        # UNDO
        self.button_undo.place(x=911, y=37, width=18.0, height=18.0)

        # SPEAKER OUTPUT BUTTON
        self.button_speaker.place(x=526, y=48, width=18.0, height=18.0)

        # EXPAND
        self.button_expand.place(x=380, y=53, width=10.0, height=8.0)

        # VOLUME BAR SPEAKERS
        self.button_speakerLvolumebar.place(x=562, y=50, width=119.0, height=7.0)
        self.button_speakerRvolumebar.place(x=562, y=57, width=119.0, height=7.0)

        # RECORD BUTTON
        self.button_record.place(x=218, y=43, width=32.0, height=32.0)
        self.button_recordactive.place(x=218, y=43, width=32.0, height=32.0)
        self.button_record.tkraise()

        # STOP BUTTON
        self.button_stop.place(x=170, y=43, width=32.0, height=32.0)

        # PAUSE BUTTON
        self.button_pause.place(x=114,y=43,width=32.0,height=32.0)

        # PLAY BUTTON
        self.button_play.place(x=66, y=43, width=32, height=32)

        # MICROPHONE
        self.button_microphone.place(x=361, y=48, width=18, height=18)

        # EXPAND MICROPHONE
        self.button_expand2.place(x=545, y=53, width=10, height=8)

        # VOLUMEBAR
        self.button_micvolumebar.place(x=397, y=53, width=119, height=7)
        self.button_micvolumebar1.place(x=397, y=53, width=119, height=7)
        self.button_micvolumebar2.place(x=397, y=53, width=119, height=7)
        self.button_micvolumebar3.place(x=397, y=53, width=119, height=7)
        self.button_micvolumebar4.place(x=397, y=53, width=119, height=7)
        self.button_micvolumebar5.place(x=397, y=53, width=119, height=7)
        self.button_micvolumebar6.place(x=397, y=53, width=119, height=7)
        self.button_micvolumebar7.place(x=397, y=53, width=119, height=7)
        self.button_micvolumebar8.place(x=397, y=53, width=119, height=7)
        self.button_micvolumebar9.place(x=397, y=53, width=119, height=7)
        self.button_micvolumebar10.place(x=397, y=53, width=119, height=7)
        self.button_micvolumebarmax.place(x=397, y=53, width=119, height=7)


    def start_record(self):
        self.button_recordactive.tkraise()
        self.create_track_ui()  # adds new track ui
        self.recorder.start_recording()


    def stop_recording(self):
        self.button_record.tkraise()
        self.recorder.stop_recording()


    def create_track_ui(self):
        """ Generates the left options box and the volume box
            Left Box:   Background (BOX)
                        Volume level (ORANGE MIDDLE)
                        Mute Display (BLUE TOP BAR)
                        PAN/GAIN BOX LEFT """

        track_id = len(self.recorder.tracks)    # which track was just created?

        if track_id == 0:
            # TRACK 0 BLUE MAIN
            canvas.create_rectangle(218, 139, 1440, 309, fill="#1D1D1D", outline="")    # BOX
            canvas.create_rectangle(218, 221, 1440, 223, fill="#9B7347", outline="")    # ORANGE MIDDLE
            canvas.create_rectangle(218, 133, 1440, 139, fill="#02ECFE", outline="")    # BLUE TOP BAR

            # Track 0 LEFT BOX
            canvas.create_rectangle(0, 133, 206, 309, fill="#1D1D1D", outline="")       # LEFT GAIN BOX
            canvas.create_rectangle(0, 133, 206, 159, fill="#292929", outline="")       # GRAY BAR
            canvas.create_rectangle(0, 133, 7, 159, fill="#02ECFE", outline="")         # BLUE BAR
            canvas.create_text(43, 139, anchor="nw", text="Track 0", fill="#5B5B5B", font=("Roboto", 12 * -1))
            self.button_solo.place(x=181, y=139, width=8, height=14)
            self.button_mute.place(x=165,y=139,width=11,height=14)
            self.button_x.place(x=14,y=142,width=7,height=8)

            # PAN
            canvas.create_text(139, 185, anchor="nw", text="Pan", fill="#A7A7A7", font=("Roboto", 12 * -1))
            self.button_pan.place(x=125, y=201, width=59, height=60)
            self.button_panR.place(x=125, y=201, width=59, height=59)
            self.button_panL.place(x=125, y=201, width=60, height=59)
            self.button_pan50R.place(x=125, y=201, width=59, height=59)
            self.button_pan50L.place(x=125, y=201, width=59, height=59)
            canvas.create_rectangle(120, 200, 200, 290, fill="#1D1D1D", outline="")  # BOX LEFT
            self.button_pan.tkraise()

            # GAIN
            canvas.create_text(44, 185, anchor="nw", text="Gain", fill="#A7A7A7", font=("Roboto", 12 * -1))
            self.button_gain.place(x=32, y=201, width=59, height=58)
            self.button_gainR.place(x=32, y=201, width=59, height=59)
            self.button_gainL.place(x=32, y=201, width=58, height=59)
            self.button_gain50R.place(x=32, y=201, width=59, height=59)
            self.button_gain50L.place(x=32, y=201, width=59, height=59)
            self.button_gain.tkraise()

            # if re recorded raise buttons to make sure they are visible
            self.button_gain.tkraise()
            self.button_pan.tkraise()
            self.button_x.tkraise()


        # Second Track
        if track_id == 1:

            # TRACK 1 PURPLE MAIN
            canvas.create_rectangle(218, 331, 1440, 501, fill="#1D1D1D", outline="")    # BOX
            canvas.create_rectangle(218, 413, 1440, 415, fill="#9B7347", outline="")    # ORANGE MIDDLE
            canvas.create_rectangle(218, 325, 1440, 331, fill="#9F40F0", outline="")    # PURPLE TOP BAR

            # Track 1 LEFT BOX
            canvas.create_rectangle(0, 325, 206, 501, fill="#1D1D1D", outline="")       # BOX LEFT
            canvas.create_rectangle(0, 325, 206, 351, fill="#292929", outline="")       # GRAY BAR
            canvas.create_rectangle(0.0, 325, 7.0, 351, fill="#9F40F0", outline="")     # PURPLE BAR
            canvas.create_text(43, 331, anchor="nw", text="Track 1", fill="#5B5B5B", font=("Roboto", 12 * -1))
            self.button_solo1.place(x=181, y=331, width=8, height=14)
            self.button_mute1.place(x=165, y=331, width=11, height=14)
            self.button_x1.place(x=14, y=334, width=7, height=8)

            # PAN
            canvas.create_text(139,377,anchor="nw",text="Pan",fill="#A7A7A7",font=("Roboto", 12 * -1))
            self.button_pan1.place(x=125, y=393, width=59, height=59)
            self.button_pan1R.place(x=125, y=393, width=59, height=59)
            self.button_pan1L.place(x=125, y=393, width=59, height=59)
            self.button_pan1_50R.place(x=125, y=393, width=59, height=59)
            self.button_pan1_50L.place(x=125, y=393, width=59, height=59)
            self.button_pan1.tkraise()

            # GAIN
            canvas.create_text(44, 377, anchor="nw", text="Gain", fill="#A7A7A7", font=("Roboto", 12 * -1))
            self.button_gain1.place(x=32, y=393,  width=59, height=57)
            self.button_gain1R.place(x=32, y=393, width=59, height=59)
            self.button_gain1L.place(x=32, y=393, width=58, height=59)
            self.button_gain1_50R.place(x=32, y=393, width=59, height=59)
            self.button_gain1_50L.place(x=32, y=393, width=59, height=59)
            self.button_gain1.tkraise()

            # if re recorded raise buttons to make sure they are visible
            self.button_gain1.tkraise()
            self.button_pan1.tkraise()
            self.button_x1.tkraise()



    def change_bitrate(self):

        # UI UPDATE
        bitstate = self.recorder.get_bitrate()
        if bitstate == True: # 16 bit (button passive)
            self.button_bitrate.lower(self.button_bitrateactive)
            print("Bitrate changed to 32")
        else:
            self.button_bitrateactive.lower(self.button_bitrate)
            print("Bitrate changed to 16")

        # RECORDER UPDATE
        self.recorder.change_bitrate()


    def change_samplingrate(self):
        """ TODO: add 48000 and 196000 """

        # UI UPDATE
        samplingstate = self.recorder.get_sampling()
        if samplingstate == 44100:   # current is 44100 will change to 96 now
            self.button_sampling.lower(self.button_samplingactive)
            print("Sampling rate changed to 96.000Hz")
        else:
            self.button_samplingactive.lower(self.button_sampling)
            print("Sampling rate changed to 44.100Hz")

        # RECORDER UPDATE
        self.recorder.change_sampling()


    def normalize(self):

        # UI UPDATE
        normalizestate = self.recorder.NORMALIZE
        if normalizestate == True:
            self.button_normalizeractive.lower(self.button_normalizer)
        else:
            self.button_normalizer.lower(self.button_normalizeractive)

        # RECORDER UPDATE
        self.recorder.normalize()

    def display_loop(self):
        window.mainloop()

    def mute_track0(self):
        """ Mutes or unmutes track 0, specific function for trakc0
            because button cant call function with argument without executing it 
            saves if track is now muted or unmuted and updates ui """
        muted = self.recorder.mute_track(0)
        if muted:
            canvas.create_rectangle(218, 133, 1440.0, 139,fill="#1D1D1D", outline="")
        else:
            canvas.create_rectangle(218, 133, 1440.0, 139,fill="#02ECFE", outline="")

    def mute_track1(self):
        muted = self.recorder.mute_track(1)
        if muted:
            canvas.create_rectangle(218, 325, 1440.0, 331, fill="#1D1D1D",outline="")
        else:
            canvas.create_rectangle(218, 325, 1440.0, 331, fill="#9F40F0",outline="")  # top bar

    def solotrack0(self):

        # basically mute every track excpet 0
        self.mute_track1()
        #self.mute_track2()
        #self.mute_track3()

    def delete_track0(self):

        # erase track 0
        self.button_gain.lower()
        self.button_gainR.lower()
        self.button_gainL.lower()
        self.button_gain50R.lower()
        self.button_gain50L.lower()
        self.button_pan.lower()
        self.button_panR.lower()
        self.button_panL.lower()
        self.button_pan50R.lower()
        self.button_pan50L.lower()
        self.button_x.lower()
        self.button_mute.lower()
        self.button_solo.lower()
        canvas.create_rectangle(0, 120, 1440.0, 320, fill="#111111", outline="")

        del self.recorder.tracks[0]


    def change_pan(self, track_id):
        self.recorder.tracks[track_id].change_pan()

        # update ui
        if track_id == 0:
            if self.recorder.tracks[track_id].PAN == 0:
                self.button_pan.tkraise()
            if self.recorder.tracks[track_id].PAN == 0.5:
                self.button_pan50R.tkraise()
            if self.recorder.tracks[track_id].PAN == 1:
                self.button_panR.tkraise()
            if self.recorder.tracks[track_id].PAN == -0.5:
                self.button_pan50L.tkraise()
            if self.recorder.tracks[track_id].PAN == -1:
                self.button_panL.tkraise()
                self.button_panR.lower()
        elif track_id == 1:
            if self.recorder.tracks[track_id].PAN == 0:
                self.button_pan1.tkraise()
            if self.recorder.tracks[track_id].PAN == 0.5:
                self.button_pan1_50R.tkraise()
            if self.recorder.tracks[track_id].PAN == 1:
                self.button_pan1R.tkraise()
            if self.recorder.tracks[track_id].PAN == -0.5:
                self.button_pan1_50L.tkraise()
            if self.recorder.tracks[track_id].PAN == -1:
                self.button_pan1L.tkraise()
                self.button_pan1R.lower()

    def change_gain(self, track_id):
        self.recorder.tracks[track_id].change_gain()

        # update ui
        if track_id == 0:
            if self.recorder.tracks[track_id].GAIN == 0:
                self.button_gain.tkraise()
            if self.recorder.tracks[track_id].GAIN == 0.5:
                self.button_gain50R.tkraise()
            if self.recorder.tracks[track_id].GAIN == 1:
                self.button_gainR.tkraise()
            if self.recorder.tracks[track_id].GAIN == -0.5:
                self.button_gain50L.tkraise()
            if self.recorder.tracks[track_id].GAIN == -1:
                self.button_gainL.tkraise()
                self.button_gainR.lower()
        elif track_id == 1:
            if self.recorder.tracks[track_id].GAIN == 0:
                self.button_gain1.tkraise()
            if self.recorder.tracks[track_id].GAIN == 0.5:
                self.button_gain1_50R.tkraise()
            if self.recorder.tracks[track_id].GAIN == 1:
                self.button_gain1R.tkraise()
            if self.recorder.tracks[track_id].GAIN == -0.5:
                self.button_gain1_50L.tkraise()
            if self.recorder.tracks[track_id].GAIN == -1:
                self.button_gain1L.tkraise()
                self.button_gain1R.lower()

    def show_micselection(self):
        """ TODO: Buttons dont work except last one """

        mics = self.recorder.get_mics()
        files = []  # creates list to replace your actual inputs for troubleshooting purposes
        btn = []    # creates list to store the buttons ins

        for i in range(len(mics)):  # this just popultes a list as a replacement for your actual inputs for troubleshooting purposes
            files.append(str(mics[i]))

        for i in range(len(files)):  # this says for *counter* in *however many elements there are in the list files*
            # the below line creates a button and stores it in an array we can call later, it will print the value of it's own text by referencing itself from the list that the buttons are stored in
            btn.append(Button(window, fg="white",text=files[i], bg = "#1D1D1D", borderwidth=0, highlightthickness=0, relief="flat",command=lambda c=i: self.recorder.switch_mic(c))) #print(btn[c].cget("text"))))
            btn[i].place(x=400, y=100+(i*50), width=180,height=50)
           # btn[i].pack()  # this packs the buttons

    def show_speakerselection(self):
        speaker = self.recorder.get_speaker()
        files = []  # creates list to replace your actual inputs for troubleshooting purposes
        btn = []  # creates list to store the buttons ins

        for i in range(
                len(speaker)):  # this just popultes a list as a replacement for your actual inputs for troubleshooting purposes
            files.append(str(speaker[i]))

        for i in range(len(files)):  # this says for *counter* in *however many elements there are in the list files*
            # the below line creates a button and stores it in an array we can call later, it will print the value of it's own text by referencing itself from the list that the buttons are stored in
            btn.append(Button(window, fg="white", text=files[i], bg="#1D1D1D", borderwidth=0, highlightthickness=0,
                              relief="flat",
                              command=lambda c=i: self.recorder.switch_speaker(c)))  # print(btn[c].cget("text"))))
            btn[i].place(x=500, y=100 + (i * 50), width=180, height=50)