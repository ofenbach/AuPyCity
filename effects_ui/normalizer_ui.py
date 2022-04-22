from tkinter import Canvas, Button
from tkinter.ttk import Scale

from PIL import Image
from PIL import ImageTk
from audio import wavefile


class NormalizerUI:

    def __init__(self, main_canvas, context):
        """ Responsible for normalizer window """
        self.main_canvas = main_canvas
        self.context = context

    def open(self):
        self.context.current_window = "normalizer"
        self.canvas = Canvas(self.main_canvas, bg="#181818", height=216, width=156, bd=0, highlightthickness=0, relief="ridge")
        self.canvas.place(x=313, y=691)

        # window ui
        self.canvas.create_rectangle(0, 0, 156, 26, fill="#292929", outline="")         # top bar grey
        self.canvas.create_rectangle(0, 0, 7, 26, fill="#02ECFE", outline="")           # top bar blue
        self.canvas.create_text(362 - 313, 699-691, anchor='nw', text='Normalizer', fill='#AFAFAF', font=('Roboto', 12))

        # selection elements
        self.canvas.create_text(328 - 313, 743 - 691, anchor='nw', text='Peak Amplitude', fill='#FFFFFF', font=('Roboto Regular', 13))
        self.slider_normalize = Scale(self.canvas, from_=-16, to=-1)
        self.slider_normalize.place(x=328-313, y=768-691, width=126, height=12)
        self.db_text = self.canvas.create_text(376 - 313, 788 - 691, anchor='nw', text="-1 Db", fill='#FFFFFF', font=('Roboto Regular', 13))

        self.image_applyall = ImageTk.PhotoImage(Image.open("effects_ui/assets/apply_all.png").resize((126, 29)))
        self.button_applyall = Button(self.canvas,image=self.image_applyall, bg="#1D1D1D", borderwidth = 0, highlightthickness = 0,
                                      command = lambda: self.apply_normalizer(True))
        self.button_applyall.place(x=328-313,y=825-691, width = 126, height=29)

        self.image_apply = ImageTk.PhotoImage(Image.open("effects_ui/assets/apply.png").resize((126, 29)))
        self.button_apply = Button(self.canvas,image=self.image_apply, bg="#1D1D1D", borderwidth = 0, highlightthickness = 0,
                                      command = lambda: self.apply_normalizer())
        self.button_apply.place(x=328-313,y=861-691, width = 126, height=29)

    def refresh(self):
        try:
            self.canvas.itemconfig(self.db_text, text=str(int(self.slider_normalize.get())) + " Db")  # slider text update
        except:
            pass

    def delete(self):
        """ Closing window by deleting every instance """
        self.slider_normalize.destroy()
        self.button_applyall.destroy()
        del self.image_applyall
        self.canvas.destroy()

        if self.context.current_window == "normalizer":
            self.context.current_window = "none"

    def apply_normalizer(self, all=False):

        for track in self.context.TRACKS:
            if track.SELECTED or all:

                try:  # try edited first
                    self.wave_mixer = wavefile.WaveFile("recordings/edited/track" + str(track.ID) + ".wav")
                except:  # otherwise use raw
                    self.wave_mixer = wavefile.WaveFile("recordings/raw/track" + str(track.ID) + ".wav")

                self.wave_mixer.normalize(self.slider_normalize.get())
                print("[NORMALIZER] Track" + str(track.ID) + " normalized.")