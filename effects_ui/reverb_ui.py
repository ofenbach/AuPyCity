from tkinter import Canvas, Button
from tkinter.ttk import Scale
from PIL.ImageTk import PhotoImage

from audio import wavefile


class ReverbUI:

    def __init__(self, main_canvas, context):
        self.main_canvas = main_canvas
        self.context = context

    def open(self):
        self.context.current_window = "reverb"
        self.canvas = Canvas(self.main_canvas, bg="#181818", height=500, width=156, bd=0, highlightthickness=0, relief="ridge")
        self.canvas.place(x=713, y=600)

        # window ui
        self.canvas.create_rectangle(0, 0, 156, 26, fill="#292929", outline="")  # top bar grey
        self.canvas.create_rectangle(0, 0, 7, 26, fill="#02ECFE", outline="")  # top bar blue
        self.canvas.create_text(451 - 402, 735 - 731, anchor='nw', text='Reverb', fill='#5B5B5B',font=('Roboto Light', 11))

        self.image_delete = PhotoImage(file="tkinterdesigner/work_frame_assets/delete.png")
        self.button_delete = Button(self.canvas, image=self.image_delete, borderwidth=0, highlightthickness=0,
                                    command=lambda: self.delete(), relief='flat')
        self.button_delete.place(x=417 - 402, y=740 - 731, width=10.0, height=10.0)

        self.canvas.create_text(417-402, 30, anchor='nw', text='Dry Level', fill='#FFFFFF', font=('Roboto Light', 12))
        self.slider_drylevel = Scale(self.canvas, from_=0, to=100)
        self.slider_drylevel.place(x=417-402, y=50, width=126, height=12)
        self.dry_level_text = self.canvas.create_text(465 - 402,120, anchor='nw', text="-1 Db", fill='#FFFFFF', font=('Roboto Regular', 13))

        self.canvas.create_text(417-402, 80, anchor='nw', text='Wet Level', fill='#FFFFFF', font=('Roboto Light', 12))
        self.slider_wetlevel = Scale(self.canvas, from_=0, to=100)
        self.slider_wetlevel.place(x=417-402, y=100, width=100, height=12)

        self.canvas.create_text(417-402, 130, anchor='nw', text='Room Size', fill='#FFFFFF', font=('Roboto Light', 12))
        self.slider_roomsize = Scale(self.canvas, from_=0, to=100)
        self.slider_roomsize.place(x=417-402,y=150, width=100,height=12)


        self.button_apply = Button(self.canvas, bg="#333333", text="Apply", borderwidth=0, highlightthickness=0, font=('Roboto Regular', 13), fg="white",
                                   command=lambda: self.apply_reverb(), relief="flat")
        self.button_apply.place(x=438 - 402, y=280, width=84, height=30)

    def apply_reverb(self):
        for track in self.context.TRACKS:
            if track.SELECTED:

                try:
                    self.wave_mixer = wavefile.WaveFile("recordings/edited/track" + str(track.ID) + ".wav")
                except:
                    print("[REVERB] Trying raw now ...")
                    self.wave_mixer = wavefile.WaveFile("recordings/raw/track" + str(track.ID) + ".wav")

                self.wave_mixer.add_reverb(room_size=self.slider_roomsize.get() / 100,
                                           wet_level=self.slider_wetlevel.get() / 100,
                                           dry_level=self.slider_drylevel.get() / 100)
                print("[REVERB] Track" + str(track.ID) + " reverbed.")

    def refresh(self):
        try:
            #elf.canvas.itemconfig(self.db_text, text=str(int(self.sli.get())) + " Db")  # slider text update
            pass
        except:
            pass

    def delete(self):
        """ Closing window by deleting every instance """
        self.canvas.destroy()
        self.button_apply.destroy()
        self.button_delete.destroy()
        self.slider_wetlevel.destroy()
        self.slider_roomsize.destroy()
        self.slider_drylevel.destroy()

        if self.context.current_window == "reverb":
            self.context.current_window = "none"

    def apply_reverb(self):
        for track in self.context.TRACKS:
            if track.SELECTED:

                try:
                    self.wave_mixer = wavefile.WaveFile("recordings/edited/track" + str(track.ID) + ".wav")
                except:
                    print("[REVERB] Trying raw now ...")
                    self.wave_mixer = wavefile.WaveFile("recordings/raw/track" + str(track.ID) + ".wav")

                self.wave_mixer.add_reverb(room_size=self.slider_roomsize.get() / 100, wet_level=self.slider_wetlevel.get() / 100, dry_level=self.slider_drylevel.get() / 100)
                print("[REVERB] Track" + str(track.ID) + " reverbed.")