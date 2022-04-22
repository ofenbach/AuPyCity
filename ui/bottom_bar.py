#!/usr/bin/env python

from tkinter import PhotoImage, Button, Canvas
from pathlib import Path
from tkinter.ttk import Scale

from effects_ui.compressor_ui import CompressorUI
from effects_ui.denoiser_ui import DenoiserUI
from effects_ui.normalizer_ui import NormalizerUI
from audio import wavefile, eq_presets

# Makes loading images easier
from effects_ui.reverb_ui import ReverbUI

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("../old/tkinterdesigner/bottom_bar/")
def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


class BottomBarUI:
    """ Contains audio settings, effects & general settings """

    def __init__(self, window, main_canvas, context):
        """ Draws all the elements in a new canvas just for the bottom bar """
        self.window = window
        self.context = context
        self.main_canvas = main_canvas

        # background canvas
        self.canvas = Canvas(window, bg="#111111", height=1000-906, width=1440, bd=0, highlightthickness=0, relief="ridge")
        self.canvas.place(x=0, y=906)
        self.canvas.create_rectangle(0, 1, 0+1440, 94, fill="#1D1D1D", outline="")    # main bottom box

        # cutter
        self.canvas.create_rectangle(319, 933-906, 319.000002, 933+45 - 906, fill="#2F2F2F", outline="")     # cutter left
        self.canvas.create_rectangle(819, 933-906, 819.000002, 933+45 - 906, fill="#2F2F2F", outline="")     # cutter mid
        self.canvas.create_rectangle(1295.0, 933-906, 1295.000002, 933+45 - 906, fill="#2F2F2F", outline="") # cutter right

        # Bitdepth
        self.image_bitdepth32 = PhotoImage(file=relative_to_assets("bitdepth32.png"))
        self.button_bitdepth32 = Button(image=self.image_bitdepth32, bg="#1D1D1D", borderwidth=0, highlightthickness=0,
                                        command=lambda: self.switch_bitdepth(), relief="flat")
        self.button_bitdepth32.place(x=37, y=906, width=82, height=94)
        self.button_bitdepth32.lower()
        self.image_bitdepth16 = PhotoImage(file=relative_to_assets("bitdepth16.png"))
        self.button_bitdepth16 = Button(image=self.image_bitdepth16, bg="#1D1D1D", borderwidth=0, highlightthickness=0,
                                        command=lambda: self.switch_bitdepth(), relief="flat")
        self.button_bitdepth16.place(x=37, y=907, width=82, height=93)

        # Sampling Rate
        self.image_sampling441 = PhotoImage(file=relative_to_assets("sampling441.png"))
        self.button_sampling441 = Button(image=self.image_sampling441, bg="#1D1D1D", borderwidth=0, highlightthickness=0,
                                         command=lambda: self.switch_sampling(), relief="flat")
        self.button_sampling441.place(x=132, y=907, width=68, height=93)
        self.image_sampling96 = PhotoImage(file=relative_to_assets("sampling_96.png"))
        self.button_sampling96 = Button(image=self.image_sampling96, bg="#1D1D1D", borderwidth=0,
                                        highlightthickness=0,
                                        command=lambda: self.switch_sampling(), relief="flat")
        self.button_sampling96.place(x=132, y=906, width=68, height=94)
        self.button_sampling96.lower()

        # Stereo
        self.image_stereo = PhotoImage(file=relative_to_assets("stereo.png"))
        self.button_stereo = Button(image=self.image_stereo, bg="#1D1D1D", borderwidth=0, highlightthickness=0,
                                    command=lambda: print("button_8 clicked"), relief="flat")
        self.button_stereo.place(x=213, y=906, width=68, height=94)

        # Normalizer
        self.image_normalizer = PhotoImage(file=relative_to_assets("normalizer.png"))
        self.button_normalizer = Button(image=self.image_normalizer, bg="#1D1D1D", borderwidth=0, highlightthickness=0,
                                   command=lambda: self.show_normalizer(), relief="flat")
        self.button_normalizer.place(x=357, y=907, width=68, height=93)

        # Compressor
        self.image_compressor = PhotoImage(file=relative_to_assets("compressor.png"))
        self.button_compressor = Button(image=self.image_compressor, bg="#1D1D1D", borderwidth=0, highlightthickness=0,
                                   command=lambda: self.show_compressor(), relief="flat")
        self.button_compressor.place(x=446, y=907, width=68, height=93)

        # Equalizer
        self.image_equalizer = PhotoImage(file=relative_to_assets("equalizer.png"))
        self.button_equalizer = Button(image=self.image_equalizer, bg="#1D1D1D", borderwidth=0, highlightthickness=0,
                                  command=lambda: self.show_equalizer_window(), relief="flat")
        self.button_equalizer.place(x=535, y=907, width=68, height=93)
        self.equalizer_expanded = False

        # Denoise
        self.image_noisefilter = PhotoImage(file=relative_to_assets("denoise.png"))
        self.button_noisefilter = Button(image=self.image_noisefilter, bg="#1D1D1D", borderwidth=0, highlightthickness=0,
                                    command=lambda: self.show_denoiser_window(), relief="flat")
        self.button_noisefilter.place(x=624, y=907, width=68, height=93)

        # Reverb
        self.image_reverb = PhotoImage(file=relative_to_assets("reverb.png"))
        self.button_reverb = Button(image=self.image_reverb, bg="#1D1D1D", borderwidth=0, highlightthickness=0,
                                   command=lambda: self.show_reverb(), relief="flat")
        self.button_reverb.place(x=713, y=907, width=68, height=93)
        self.reverb_expanded = False    # signal if window already opened

        # Donate
        self.image_donate = PhotoImage(file=relative_to_assets("donate.png"))
        self.button_donate = Button(image=self.image_donate, bg="#1D1D1D", borderwidth=0, highlightthickness=0,
                                    command=lambda: print("button_3 clicked"), relief="flat")
        self.button_donate.place(x=1194, y=907, width=68, height=93)

        # Settings
        self.image_settings = PhotoImage(file=relative_to_assets("settings.png"))
        self.button_settings = Button(image=self.image_settings, bg="#1D1D1D", borderwidth=0, highlightthickness=0,
                                      command=lambda: print("button_1 clicked"), relief="flat")
        self.button_settings.place(x=1333, y=907, width=68, height=93)

        # effect effects_ui
        self.normalizer_window = NormalizerUI(self.main_canvas, self.context)
        self.compressor_window = CompressorUI(self.main_canvas, self.context)
        self.reverb_window = ReverbUI(self.main_canvas, self.context)
        self.normalizer_window = NormalizerUI(self.main_canvas, self.context)
        self.denoiser_window = DenoiserUI(self.main_canvas, self.context)


    """ MAIN LOOP """
    def refresh(self):
        if self.context.current_window == "normalizer":
            self.normalizer_window.refresh()
        if self.context.current_window == "denoiser":
            self.denoiser_window.refresh()

    """ AUDIO SETTINGS """
    def switch_sampling(self):
        """ Switches sampling from 44.100 to 96.000 or back """
        if self.context.sampling == 96000:
            self.context.sampling = 44100
            self.button_sampling441.tkraise()
            self.button_sampling96.lower()
        else:
            self.context.sampling = 96000
            self.button_sampling96.tkraise()
    def switch_bitdepth(self):
        """ Switches bitdepth from 16 to 32 or back """
        if self.context.bitdepth == 16:
            self.context.bitdepth = 32
            self.button_bitdepth32.tkraise()
        else:
            self.context.bitdepth = 16
            self.button_bitdepth16.tkraise()
            self.button_bitdepth32.lower()


    """ EFFECTS WINDOWS """
    def show_normalizer(self):
        if self.context.current_window != "normalizer":
            try:
                self.compressor_window.delete()
                self.reverb_window.delete()
            except Exception as e:
                print("[ERROR] deleting other effect effects_ui")
                print(e)
            self.normalizer_window.open()
        elif self.context.current_window == "normalizer":
            self.normalizer_window.delete()

    def show_compressor(self):
        if self.context.current_window != "compressor":
            try:
                self.normalizer_window.delete()
                self.reverb_window.delete()
            except Exception as e:
                print("[ERROR] deleting other effect effects_ui")
            self.compressor_window.open()
        elif self.context.current_window == "compressor":
            self.compressor_window.delete()

    def show_reverb(self):
        if self.context.current_window != "reverb":
            try:
                self.normalizer_window.delete()
                self.compressor_window.delete()
            except Exception as e:
                print("[ERROR] deleting other effect effects_ui")
            self.reverb_window.open()
        elif self.context.current_window == "reverb":
            self.reverb_window.delete()


    def show_denoiser_window(self):
        if self.context.current_window != "denoiser":
            try:
                self.normalizer_window.delete()
                self.reverb_window.delete()
            except Exception as e:
                print("[ERROR] deleting other effect effects_ui")
            self.denoiser_window.open()
        elif self.context.current_window == "denoiser":
            self.denoiser_window.delete()
        """if self.current_window_opened == "none":
            self.current_window_opened = "denoiser"
            self.context.DELETE_HINTS = True

            # window
            self.main_canvas.create_rectangle(402,731,402+156,731+176, fill="#181818", outline="")          # main box
            self.main_canvas.create_rectangle(402, 731, 402 + 156, 731 + 26, fill="#292929", outline="")    # top bar grey
            self.main_canvas.create_rectangle(402, 731, 402 + 7, 731 + 26, fill="#02ECFE", outline="")    # top bar blue
            self.main_canvas.create_text(451, 735, anchor='nw', text='Denoiser', fill='#5B5B5B', font=('Roboto Light', 11))
            self.image_delete = PhotoImage(file="tkinterdesigner/work_frame_assets/delete.png")
            self.button_delete = Button(image=self.image_delete, borderwidth=0, highlightthickness=0,
                                        command=lambda: self.show_compress_window(), relief='flat')
            self.button_delete.place(x=417.0, y=740, width=10.0, height=10.0)

            # selection
            self.main_canvas.create_text(417, 789, anchor='nw', text='Reduction in %', fill='#FFFFFF', font=('Roboto Regular', 13))
            self.slider_reduction = Scale(self.main_canvas, from_=0, to=100)
            self.slider_reduction.place(x=417, y=814, width=126, height=12)
            self.db_text = self.main_canvas.create_text(465, 834, anchor='nw', text=str(int(self.slider_reduction.get()))+" %" + ' Db', fill='#FFFFFF', font=('Roboto Regular', 13))
            self.button_apply = Button(bg="#333333", text="Apply", borderwidth=0, highlightthickness=0,
                                       font=('Roboto Regular', 13), fg="white",
                                       command=lambda: self.reduce_noise(), relief="flat")
            self.button_apply.place(x=438, y=868, width=84, height=20)

        elif self.current_window_opened == "denoiser":
            self.current_window_opened == "none"
            pass # delete UI"""


    def reduce_noise(self):
        """ Reduces noise
            TODO: Add sensitivity option """
        for track in self.context.TRACKS:
            if track.SELECTED:

                try:
                    self.wave_mixer = wavefile.WaveFile("recordings/edited/track" + str(track.ID) + ".wav")
                except Exception as e:
                    print("trying raw " , e)
                    self.wave_mixer = wavefile.WaveFile("recordings/raw/track" + str(track.ID) + ".wav")

                self.wave_mixer.noise_filter(reduction=self.slider_reduction.get()/100)
                print("[NOISE] Track" + str(track.ID) + " denoised.")







    def show_equalizer_window(self):
        # open equalizer window
        if self.current_window_opened == "none":
            self.current_window_opened = "equalizer"
            self.context.DELETE_HINTS = True

            self.main_canvas.create_rectangle(358, 441, 358+702, 441+476, fill="#212121", outline="")       # window box
            self.main_canvas.create_rectangle(358, 441, 358 + 702, 441 + 26, fill="#292929", outline="")    # top bar
            self.main_canvas.create_rectangle(358, 441, 358 + 7, 441 + 26, fill="#02ECFE", outline="")      # blue bar

            self.image_delete = PhotoImage(file="../old/tkinterdesigner/work_frame_assets/delete.png")
            self.button_delete = Button(image=self.image_delete, borderwidth=0, highlightthickness=0,
                                        command=lambda: self.show_equalizer_window(), relief='flat')
            self.button_delete.place(x=372.0, y=450, width=10.0, height=10.0)

            from PIL import ImageTk
            from PIL import Image
            self.image_vintage = ImageTk.PhotoImage(Image.open("../old/tkinterdesigner/presets/vintage.png").resize((64, 92)))
            self.button_vintage = Button(image=self.image_vintage, borderwidth=0, highlightthickness=0,
                                         command=lambda: eq_presets.apply_vintage(self.sliders_eq), relief='flat')
            self.button_vintage.place(x=450, y=497, width=64, height=92)

            self.image_eguitar = ImageTk.PhotoImage(Image.open(
                "../old/tkinterdesigner/presets/electric_guitar.png").resize((64, 92)))
            self.button_eguitar = Button(image=self.image_eguitar, borderwidth=0, highlightthickness=0,
                                         command=lambda: eq_presets.apply_eguitar(self.sliders_eq), relief='flat')
            self.button_eguitar.place(x=541, y=497, width=64, height=92)

            self.image_aguitar = ImageTk.PhotoImage(Image.open(
                "../old/tkinterdesigner/presets/acoustic_guitar.png").resize((64, 92)))
            self.button_aguitar = Button(image=self.image_aguitar, borderwidth=0, highlightthickness=0,
                                         command=lambda: eq_presets.apply_aguitar(self.sliders_eq), relief='flat')
            self.button_aguitar.place(x=632, y=497, width=64, height=92)

            self.image_piano = ImageTk.PhotoImage(Image.open("../old/tkinterdesigner/presets/piano.png").resize((64, 92)))
            self.button_piano = Button(image=self.image_piano, borderwidth=0, highlightthickness=0,
                                       command=lambda: eq_presets.apply_piano(self.sliders_eq), relief='flat')
            self.button_piano.place(x=723, y=497, width=64, height=92)

            self.image_vocals = ImageTk.PhotoImage(Image.open("../old/tkinterdesigner/presets/vocals.png").resize((64, 92)))
            self.button_vocals = Button(image=self.image_vocals, borderwidth=0, highlightthickness=0, bg="#212121",
                                        command=lambda: eq_presets.apply_vocals(self.sliders_eq), relief='flat')
            self.button_vocals.place(x=814, y=497, width=64, height=92)

            self.image_bassy = ImageTk.PhotoImage(Image.open("../old/tkinterdesigner/presets/bass.png").resize((64, 92)))
            self.button_bassy = Button(image=self.image_bassy, borderwidth=0, highlightthickness=0, bg="#212121",
                                       command=lambda: eq_presets.apply_bassy(self.sliders_eq), relief='flat')
            self.button_bassy.place(x=901, y=497, width=64, height=92)

            self.image_bands = ImageTk.PhotoImage(Image.open("../old/tkinterdesigner/presets/frequencies.png").resize((585, 14)))
            self.button_bands = Button(image=self.image_bands, borderwidth=0, highlightthickness=0, bg="#212121",
                                        command=lambda: self.apply_vintage(), relief='flat')
            self.button_bands.place(x=417, y=812, width=585, height=14)

            # scale
            self.slider_20hz = Scale(self.main_canvas, from_=-12, to=12, orient="vertical")
            self.slider_20hz.place(x=411,y=650, width=20,height=120)
            self.slider_30hz = Scale(self.main_canvas, from_=-12, to=12, orient="vertical")
            self.slider_30hz.place(x=411+34*1,y=650, width=20,height=120)
            self.slider_80hz = Scale(self.main_canvas, from_=-12, to=12, orient="vertical")
            self.slider_80hz.place(x=411+34*2,y=650, width=20,height=120)
            self.slider_100hz = Scale(self.main_canvas, from_=-12, to=12, orient="vertical")
            self.slider_100hz.place(x=411+34*3,y=650, width=20,height=120)
            self.slider_125hz = Scale(self.main_canvas, from_=-12, to=12, orient="vertical")
            self.slider_125hz.place(x=411+34*4,y=650, width=20,height=120)
            self.slider_500hz = Scale(self.main_canvas, from_=-12, to=12, orient="vertical")
            self.slider_500hz.place(x=411+34*5,y=650, width=20,height=120)
            self.slider_800hz = Scale(self.main_canvas, from_=-12, to=12, orient="vertical")
            self.slider_800hz.place(x=411+34*6,y=650, width=20,height=120)
            self.slider_900hz = Scale(self.main_canvas, from_=-12, to=12, orient="vertical")
            self.slider_900hz.place(x=411+34*7,y=650, width=20,height=120)
            self.slider_1000hz = Scale(self.main_canvas, from_=-12, to=12, orient="vertical")
            self.slider_1000hz.place(x=411+34*8,y=650, width=20,height=120)
            self.slider_1500hz = Scale(self.main_canvas, from_=-12, to=12, orient="vertical")
            self.slider_1500hz.place(x=411+34*9,y=650, width=20,height=120)
            self.slider_2000hz = Scale(self.main_canvas, from_=-12, to=12, orient="vertical")
            self.slider_2000hz.place(x=411+34*10,y=650, width=20,height=120)
            self.slider_4000hz = Scale(self.main_canvas, from_=-12, to=12, orient="vertical")
            self.slider_4000hz.place(x=411+34*11,y=650, width=20,height=120)
            self.slider_5000hz = Scale(self.main_canvas, from_=-12, to=12, orient="vertical")
            self.slider_5000hz.place(x=411+34*12,y=650, width=20,height=120)
            self.slider_8000hz = Scale(self.main_canvas, from_=-12, to=12, orient="vertical")
            self.slider_8000hz.place(x=411+34*13,y=650, width=20,height=120)
            self.slider_10000hz = Scale(self.main_canvas, from_=-12, to=12, orient="vertical")
            self.slider_10000hz.place(x=411+34*14,y=650, width=20,height=120)
            self.slider_12500hz = Scale(self.main_canvas, from_=-12, to=12, orient="vertical")
            self.slider_12500hz.place(x=411+34*15,y=650, width=20,height=120)
            self.slider_16000hz = Scale(self.main_canvas, from_=-12, to=12, orient="vertical")
            self.slider_16000hz.place(x=411+34*16,y=650, width=20,height=120)
            self.slider_20000hz = Scale(self.main_canvas, from_=-12, to=12, orient="vertical")
            self.slider_20000hz.place(x=411+34*17,y=650, width=20,height=120)
            self.sliders_eq = [self.slider_20hz, self.slider_30hz, self.slider_80hz, self.slider_100hz,
                               self.slider_125hz, self.slider_500hz, self.slider_800hz, self.slider_900hz,
                               self.slider_1000hz, self.slider_1500hz, self.slider_2000hz, self.slider_4000hz,
                               self.slider_5000hz, self.slider_8000hz, self.slider_10000hz, self.slider_12500hz,
                               self.slider_16000hz, self.slider_20000hz]

            self.button_apply = Button(bg="#414141", text="Apply", borderwidth=0, highlightthickness=0,
                                       font=('Roboto Light', 16), fg="white",
                                       command=lambda: self.apply_equalizer(), relief="flat")
            self.button_apply.place(x=900,y=830, width=100, height=60)
        elif self.current_window_opened == "equalizer":
            self.current_window_opened = "none"
            # TODO: Redraw tracks, maybe instead of drawing rectangles in the first place, drawing a label that you destroy then. or new canvas
            self.main_canvas.create_rectangle(358, 441, 358 + 702, 441 + 476, fill="#111111", outline="")  # window box
            self.button_vintage.destroy()
            self.button_eguitar.destroy()
            self.button_aguitar.destroy()
            self.button_piano.destroy()
            self.button_vocals.destroy()
            self.button_bassy.destroy()
            self.button_bands.destroy()
            self.button_delete.destroy()


    def apply_equalizer(self):
        print("Equalized wav with: ")
        print(eq_presets.active_set)

        for track in self.context.TRACKS:
            if track.SELECTED:

                try:
                    self.wave_mixer = wavefile.WaveFile("recordings/edited/track" + str(track.ID) + ".wav")
                except Exception as e:
                    print("trying raw " , e)
                    self.wave_mixer = wavefile.WaveFile("recordings/raw/track" + str(track.ID) + ".wav")

                # TODO apply equalizer
                # equalizer.eq(filename, presets.active_set)

                print("[EQ] Track" + str(track.ID) + " equalized.")
