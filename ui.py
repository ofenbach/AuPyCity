import threading
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage

from recorder import Recorder

# PATH STUFF
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")
def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

# CREATE TK WINDOW
window = Tk()
window.geometry("1440x1000")
window.configure(bg="#111111")
canvas = Canvas(window,bg="#111111",height=1000,width=1440,bd=0,highlightthickness=0,relief="ridge")
canvas.place(x=0, y=0)

window.resizable(False, False)

class UI:

    def __init__(self):
        """ Initialize Recorder """
        self.recorder = Recorder()

    def load_ui(self):
        print("[UI] LOADING UI ELEMENTS")

        # LOAD IMAGES
        self.img_normalizer = PhotoImage(file=relative_to_assets("normalizer.png"))
        self.img_noisereduction = PhotoImage(file=relative_to_assets("noise_reduction.png"))
        self.img_compressor = PhotoImage(file=relative_to_assets("compressor.png"))
        self.img_sampling = PhotoImage(file=relative_to_assets("sampling_rate.png"))
        self.img_bitdepth = PhotoImage(file=relative_to_assets("bitdepth.png"))
        self.img_stereo = PhotoImage(file=relative_to_assets("stereo.png"))
        self.img_gain = PhotoImage(file=relative_to_assets("gain.png"))
        self.img_pan = PhotoImage(file=relative_to_assets("pan.png"))
        self.img_solo = PhotoImage(file=relative_to_assets("solo.png"))
        self.img_mute = PhotoImage(file=relative_to_assets("mute.png"))
        self.img_x = PhotoImage(file=relative_to_assets("x.png"))
        self.img_pan3 = PhotoImage(file=relative_to_assets("pan.png"))
        self.img_timeaxis = PhotoImage(file=relative_to_assets("time_axis.png"))
        self.img_ear = PhotoImage(file=relative_to_assets("ear.png"))
        self.img_redo = PhotoImage(file=relative_to_assets("redo.png"))
        self.img_play = PhotoImage(file=relative_to_assets("play.png"))
        self.img_pause = PhotoImage(file=relative_to_assets("pause.png"))
        self.img_stop = PhotoImage(file=relative_to_assets("stop.png"))
        self.img_record = PhotoImage(file=relative_to_assets("record.png"))
        self.img_microphone = PhotoImage(file=relative_to_assets("microphone.png"))
        self.img_volumebar = PhotoImage(file=relative_to_assets("volume_bar.png"))
        self.img_expand = PhotoImage(file=relative_to_assets("expand.png"))
        self.img_speaker = PhotoImage(file=relative_to_assets("speaker.png"))
        self.img_undo = PhotoImage(file=relative_to_assets("undo.png"))

        # LOAD BUTTONS
        self.button_noise = Button(image=self.img_noisereduction, borderwidth=0, highlightthickness=0, relief="flat",
                                   command=lambda: print("noise reduction"), )
        self.button_normalizer = Button(image=self.img_normalizer, borderwidth=0, highlightthickness=0, relief="flat",
                                        command=lambda: print("normalizer clicked"))
        self.button_compressor = Button(image=self.img_compressor, borderwidth=0, highlightthickness=0, relief="flat",
                                        command=lambda: print("compressor clicked"), )
        self.button_stereo = Button(image=self.img_stereo, borderwidth=0, highlightthickness=0, relief="flat",
                                    command=lambda: print("stereo clicked"), )
        self.button_sampling = Button(image=self.img_sampling, borderwidth=0, highlightthickness=0, relief="flat",
                                      command=lambda: print("samplingrate clicked"), )
        self.button_bitdepth = Button(image=self.img_bitdepth, borderwidth=0, highlightthickness=0, relief="flat",
                                      command=lambda: print("bitdepth clicked"))
        self.button_pan = Button(image=self.img_pan,borderwidth=0,highlightthickness=0,relief="flat",
                                 command=lambda: print("Pan changed"))
        self.button_gain = Button(image=self.img_gain,borderwidth=0,highlightthickness=0, relief="flat",
                                  command=lambda: print("Gain"))
        self.button_solo = Button(image=self.img_solo,borderwidth=0,highlightthickness=0,relief="flat",
                                  command=lambda: print("solo1 clicked"))
        self.button_mute = Button(image=self.img_mute,borderwidth=0,highlightthickness=0,relief="flat",
                                  command=lambda: print("mute1 clicked"))
        self.button_x = Button(image=self.img_x,borderwidth=0,highlightthickness=0,relief="flat",
                               command=lambda: print("track1 deleted"))

    def display_default_ui(self):
        """ Loads standard AuPyCity """

        print("[UI] DISPLAYING DEFAULT UI")

        # BOTTOM BAR BOX
        canvas.create_rectangle(
            1.1368683772161603e-13,
            917.0,
            1440.0,
            1000.0,
            fill="#1D1D1D",
            outline="")

        # BOTTOM BAR TEXTAREA
        canvas.create_rectangle(
            1278.0,
            945.0,
            1418.0,
            974.0,
            fill="#1D1D1D",
            outline="")

        # BOTTOM BAR TEXTAREA BOX
        entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
        entry_bg_1 = canvas.create_image(
            1306.0,
            959.5,
            image=entry_image_1
        )
        # text inside textarea
        entry_1 = Text(
            bd=0,
            bg="#393939",
            highlightthickness=0
        )
        entry_1.place(
            x=1238.0,
            y=945.0,
            width=136.0,
            height=27.0
        )

        # BOTTOM BAR NOISE REDUCTION
        self.button_noise.place(
            x=778.9999999999999,
            y=928.0,
            width=73.0,
            height=60.0)

        # NORMALIZER
        self.button_normalizer.place(
            x=693.9999999999999,
            y=928.0,
            width=52.0,
            height=60.0)

        # COMPRESSOR
        self.button_compressor.place(
            x=594.9999999999999,
            y=928.0,
            width=57.0,
            height=60.0)

        # STEREO
        self.button_stereo.place(
            x=198.9999999999999,
            y=929.0,
            width=59.0,
            height=59.0)

        # SAMPLING RATE
        self.button_sampling.place(
            x=107.99999999999989,
            y=929.0,
            width=60.0,
            height=59.0)

        # BITDEPTH
        self.button_bitdepth.place(
            x=28.999999999999886,
            y=927.0,
            width=47.0,
            height=59.0)

        # TOP BAR
        # TIME AXIS
        self.button_timeaxis = Button(
            image=self.img_timeaxis,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_27 clicked"),
            relief="flat"
        )
        self.button_timeaxis.place(
            x=217.9999999999999,
            y=95.00000000000006,
            width=1280.0,
            height=22.0
        )

        # TIME TEXT
        # BOX TIME TODO
        canvas.create_text(
            65.99999999999989,
            99.00000000000006,
            anchor="nw",
            text="00:00:00.000",
            fill="#FFFFFF",
            font=("Roboto", 12 * -1)
        )

        # BOX TIME
        canvas.create_rectangle(
            0.0,
            23.000000000000057,
            1440.0,
            95.00000000000006,
            fill="#1D1D1D",
            outline="")

        # EAR DIRECT MONITORING
        self.button_ear = Button(
            image=self.img_ear,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("direct monitoring clicked"),
            relief="flat"
        )
        self.button_ear.place(
            x=910.9999999999999,
            y=63.00000000000006,
            width=18.0,
            height=18.0
        )

        # REDO
        self.button_redo = Button(
            image=self.img_redo,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("redo clicked"),
            relief="flat"
        )
        self.button_redo.place(
            x=934.9999999999999,
            y=37.00000000000006,
            width=18.0,
            height=18.0
        )

        # UNDO
        self.button_undo = Button(
            image=self.img_undo,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("undo clicked"),
            relief="flat"
        )
        self.button_undo.place(
            x=910.9999999999999,
            y=37.00000000000006,
            width=18.0,
            height=18.0
        )

        # SPEAKER OUTPUT BUTTON
        self.button_speaker = Button(
            image=self.img_speaker,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("speaker clicked"),
            relief="flat"
        )
        self.button_speaker.place(
            x=525.9999999999999,
            y=48.00000000000006,
            width=18.0,
            height=18.0
        )

        # EXPAND
        self.button_expand = Button(
            image=self.img_expand,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("expand clicked"),
            relief="flat"
        )
        self.button_expand.place(
            x=379.9999999999999,
            y=53.00000000000006,
            width=10.0,
            height=8.0
        )

        # VOLUME BAR
        self.button_volumebar = Button(
            image=self.img_volumebar,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("volumebar clicked"),
            relief="flat"
        )
        self.button_volumebar.place(
            x=561.9999999999999,
            y=50.00000000000006,
            width=119.0,
            height=7.0
        )

        self.volume_bar2 = Button(
            image=self.img_volumebar,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("volumebar2 clicked"),
            relief="flat"
        )
        self.volume_bar2.place(
            x=561.9999999999999,
            y=57.00000000000006,
            width=119.0,
            height=7.0
        )

        # RECORD BUTTON
        self.button_record = Button(
            image=self.img_record,
            borderwidth=0,
            highlightthickness=0,
            command=self.start_record,
            relief="flat"
        )
        self.button_record.place(
            x=217.9999999999999,
            y=43.00000000000006,
            width=32.0,
            height=32.0
        )

        # STOP BUTTON
        self.button_stop = Button(
            image=self.img_stop,
            borderwidth=0,
            highlightthickness=0,
            command=self.recorder.stop_recording,
            relief="flat"
        )
        self.button_stop.place(
            x=169.9999999999999,
            y=43.00000000000006,
            width=32.0,
            height=32.0
        )

        # PAUSE BUTTON
        self.button_pause = Button(
            image=self.img_pause,
            borderwidth=0,
            highlightthickness=0,
            command=self.recorder.pause_track,
            relief="flat"
        )
        self.button_pause.place(
            x=113.99999999999989,
            y=43.00000000000006,
            width=32.0,
            height=32.0
        )

        # PLAY BUTTON
        self.button_play = Button(
            image=self.img_play,
            borderwidth=0,
            highlightthickness=0,
            command=self.recorder.play_track,
            relief="flat"
        )
        self.button_play.place(
            x=65.99999999999989,
            y=43.00000000000006,
            width=32.0,
            height=32.0
        )

        # MICROPHONE
        self.button_microphone = Button(
            image=self.img_microphone,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("microphone clicked"),
            relief="flat"
        )
        self.button_microphone.place(
            x=360.9999999999999,
            y=48.00000000000006,
            width=18.0,
            height=18.0
        )

        # EXPAND MICROPHONE
        self.button_expand2 = Button(
            image=self.img_expand,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("expand2 clicked"),
            relief="flat"
        )
        self.button_expand2.place(
            x=544.9999999999999,
            y=53.00000000000006,
            width=10.0,
            height=8.0
        )

        # VOLUMEBAR
        self.button_volumebar2 = Button(
            image=self.img_volumebar,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("volumebar2 clicked"),
            relief="flat"
        )
        self.button_volumebar2.place(
            x=396.9999999999999,
            y=53.00000000000006,
            width=119.0,
            height=7.0
        )

    def start_record(self):
        self.create_track_ui()  # adds new track ui
        threading.Thread(target=self.recorder.start_recording).start()  # start backend recording as thread

    def create_track_ui(self):
        # TRACK 1 BOX
        canvas.create_rectangle(
            217.9999999999999,
            139.00000000000006,
            1440.0,
            309.00000000000006,
            fill="#1D1D1D",
            outline="")

        # TRACK 1 ORANGE
        canvas.create_rectangle(
            217.9999999999999,
            221.00000000000006,
            1440.0,
            223.00000000000006,
            fill="#9B7347",
            outline="")

        # TRACK 1 TOP BAR
        canvas.create_rectangle(
            217.9999999999999,
            133.00000000000006,
            1440.0,
            139.00000000000006,
            fill="#02ECFE",
            outline="")

        # TRACK 1 LEFT BOX
        canvas.create_rectangle(
            0.0,
            133.00000000000006,
            206.0,
            309.00000000000006,
            fill="#1D1D1D",
            outline="")

        # PAN 1
        canvas.create_text(
            138.9999999999999,
            185.00000000000006,
            anchor="nw",
            text="Pan",
            fill="#A7A7A7",
            font=("Roboto", 12 * -1)
        )

        # PAN1 BUTTON
        self.button_pan.place(
            x=124.99999999999989,
            y=201.00000000000006,
            width=49.0,
            height=57.0
        )

        # GAIN 1 TEXT
        canvas.create_text(
            43.999999999999886,
            185.00000000000006,
            anchor="nw",
            text="Gain",
            fill="#A7A7A7",
            font=("Roboto", 12 * -1)
        )

        # GAIN 1 BUTTON
        self.button_gain.place(
            x=31.999999999999886,
            y=201.00000000000006,
            width=49.0,
            height=57.0
        )

        # TRACK 1 LEFT BOX
        canvas.create_rectangle(
            0.0,
            133.00000000000006,
            206.0,
            159.00000000000006,
            fill="#292929",
            outline="")

        # SOLO 1
        self.button_solo.place(
            x=180.9999999999999,
            y=139.00000000000006,
            width=8.0,
            height=14.0
        )

        # MUTE 1
        self.button_mute.place(
            x=164.9999999999999,
            y=139.00000000000006,
            width=11.0,
            height=14.0
        )

        # TRACK 1 TEXT
        canvas.create_text(
            42.999999999999886,
            139.00000000000006,
            anchor="nw",
            text="Track 1",
            fill="#5B5B5B",
            font=("Roboto", 12 * -1)
        )

        # X1
        self.button_x.place(
            x=13.999999999999886,
            y=142.00000000000006,
            width=7.0,
            height=8.0
        )

        # TRACK 0 LEFT BOX TOP BAR
        canvas.create_rectangle(
            0.0,
            133.00000000000006,
            7.0,
            159.00000000000006,
            fill="#02ECFE",
            outline="")

    def display_loop(self):
        window.mainloop()