from tkinter import Canvas, Button
from tkinter.ttk import Scale

from PIL import Image
from PIL import ImageTk
from audio import wavefile


class DenoiserUI:

    def __init__(self, main_canvas, context):
        """ Responsible for normalizer window """
        self.main_canvas = main_canvas
        self.context = context

    def open(self):
        self.context.current_window = "denoiser"
        self.canvas = Canvas(self.main_canvas, bg="#181818", height=216, width=156, bd=0, highlightthickness=0, relief="ridge")
        self.canvas.place(x=624, y=691)

        # window ui
        self.canvas.create_rectangle(0, 0, 156, 26, fill="#292929", outline="")         # top bar grey
        self.canvas.create_rectangle(0, 0, 7, 26, fill="#02ECFE", outline="")           # top bar blue
        self.canvas.create_text(362 - 313, 699-691, anchor='nw', text='Denoiser', fill='#AFAFAF', font=('Roboto', 12))

        # selection elements
        self.canvas.create_text(328 - 313, 743 - 691, anchor='nw', text='Sensitivity', fill='#FFFFFF', font=('Roboto Regular', 13))
        self.slider_sensitivity = Scale(self.canvas, from_=0, to=100)
        self.slider_sensitivity.place(x=328-313, y=768-691, width=126, height=12)
        self.db_text = self.canvas.create_text(376 - 313, 788 - 691, anchor='nw', text="0%", fill='#FFFFFF', font=('Roboto Regular', 13))

        self.image_applyall = ImageTk.PhotoImage(Image.open("effects_ui/assets/apply_all.png").resize((126, 29)))
        self.button_applyall = Button(self.canvas,image=self.image_applyall, bg="#1D1D1D", borderwidth = 0, highlightthickness = 0,
                                      command = lambda: self.apply_denoiser(True))
        self.button_applyall.place(x=328-313,y=825-691, width = 126, height=29)

        self.image_apply = ImageTk.PhotoImage(Image.open("effects_ui/assets/apply.png").resize((126, 29)))
        self.button_apply = Button(self.canvas,image=self.image_apply, bg="#1D1D1D", borderwidth = 0, highlightthickness = 0,
                                      command = lambda: self.apply_denoiser())
        self.button_apply.place(x=328-313,y=861-691, width = 126, height=29)

    def refresh(self):
        try:
            self.canvas.itemconfig(self.db_text, text=str(int(self.slider_sensitivity.get())) + "%")  # slider text update
        except:
            pass

    def delete(self):
        """ Closing window by deleting every instance """
        self.slider_sensitivity.destroy()
        self.button_applyall.destroy()
        del self.image_applyall
        self.canvas.destroy()

        if self.context.current_window == "denoiser":
            self.context.current_window = "none"

    def apply_denoiser(self, all=False):

        for track in self.context.TRACKS:
            if track.SELECTED:

                try:
                    self.wave_mixer = wavefile.WaveFile("recordings/edited/track" + str(track.ID) + ".wav")
                except Exception as e:
                    print("trying raw ", e)
                    self.wave_mixer = wavefile.WaveFile("recordings/raw/track" + str(track.ID) + ".wav")

                self.wave_mixer.noise_filter(reduction=self.slider_reduction.get() / 100)
                print("[DENOISER] Track" + str(track.ID) + " denoised with ", str(self.slider_normalize.get()), "%")