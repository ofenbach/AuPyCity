from tkinter import Canvas, Button
from tkinter.ttk import Scale
from PIL.ImageTk import PhotoImage

from libs import wavefile


class CompressorUI:

    def __init__(self, main_canvas, context):
        self.main_canvas = main_canvas
        self.context = context

    def open(self):
        self.context.current_window = "compressor"
        self.canvas = Canvas(self.main_canvas, bg="#FFFFFF", height=176, width=156, bd=0, highlightthickness=0, relief="ridge")
        self.canvas.place(x=402, y=731)

        # window
        self.canvas.create_rectangle(0, 0, 156, 176, fill="#181818", outline="")  # main box
        self.canvas.create_rectangle(0, 0, 156, 26, fill="#292929", outline="")  # top bar grey
        self.canvas.create_rectangle(0, 0, 7, 26, fill="#02ECFE", outline="")  # top bar blue
        self.canvas.create_text(451-402, 735-731, anchor='nw', text='Compressor', fill='#5B5B5B',font=('Roboto Light', 11))
        self.image_delete = PhotoImage(file="tkinterdesigner/work_frame_assets/delete.png")
        self.button_delete = Button(self.canvas, image=self.image_delete, borderwidth=0, highlightthickness=0,
                                    command=lambda: self.delete(), relief='flat')
        self.button_delete.place(x=417-402, y=740-731, width=10.0, height=10.0)

        # selection
        self.canvas.create_text(417-402, 789-731, anchor='nw', text='Threshold', fill='#FFFFFF',font=('Roboto Regular', 13))
        self.slider_threshold = Scale(self.canvas, from_=-16, to=-1)
        self.slider_threshold.place(x=417-402, y=814-731, width=126, height=12)
        self.db_text = self.canvas.create_text(465-402, 834-731, anchor='nw',text=str(int(self.slider_threshold.get())) + " Db" + ' Db',fill='#FFFFFF', font=('Roboto Regular', 13))
        self.button_apply = Button(self.canvas, bg="#333333", text="Apply", borderwidth=0, highlightthickness=0,font=('Roboto Regular', 13), fg="white", command=lambda: self.compress(), relief="flat")
        self.button_apply.place(x=438-402, y=858-731, width=84, height=30)

    def refresh(self):
        try:
            self.canvas.itemconfig(self.db_text, text=str(int(self.slider_threshold.get())) + " Db")  # slider text update
        except:
            pass

    def delete(self):
        """ Closing window by deleting every instance """
        self.canvas.destroy()
        self.button_apply.destroy()
        self.button_delete.destroy()
        self.slider_threshold.destroy()

        if self.context.current_window == "compressor":
            self.context.current_window = "none"

    def apply_compressor(self):
        for track in self.context.TRACKS:
            if track.SELECTED:

                try:
                    self.wave_mixer = wavefile.WaveFile("recordings/edited/track" + str(track.ID) + ".wav")
                except:
                    print("[COMPRESS] Trying raw now ...")
                    self.wave_mixer = wavefile.WaveFile("recordings/raw/track" + str(track.ID) + ".wav")

                self.wave_mixer.compress(threshold_db=self.slider_threshold.get())
                print("[COMPRESSOR] Track" + str(track.ID) + " compressed.")