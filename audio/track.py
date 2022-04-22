#!/usr/bin/env python

from pathlib import Path
from tkinter import Button, PhotoImage
from pydub import AudioSegment

from audio.microphone import Microphone

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("../old/tkinterdesigner/work_frame_assets")
def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


class MonoTrack:

    def __init__(self, window,canvas,context, filename=""):
        self.window = window
        self.context = context
        self.canvas = canvas
        self.filename = filename

        self.mic = Microphone(self.context)

        # find out Id
        used_ids = {0: False, 1: False, 2: False, 3: False}
        if 4 > len(self.context.TRACKS) >= 0:
            for track in self.context.TRACKS:
                used_ids[track.ID] = True

            for (id, used) in used_ids.items():
                if used_ids[id] == False:
                    self.ID = id
                    break
        else:
            self.ID = 4

        # SETUP
        self.x = 0
        self.y = 141+(192*self.ID)    # blue0: 141 purple1: 333 2: 525 3: 717-722
        colors = ["#02ECFE", "#9F40F0", "#0FE511", "#FF5AD4", "#02ECFE"]
        self.color = colors[self.ID]
        self.SELECTED = False

        # AUDIO
        self.PAN = 0
        self.GAIN = 0
        self.MUTE = False
        self.SOLO = False

        # TRACK BOX
        canvas.create_rectangle(218.0, self.y+5, 1440.0, self.y+171, fill='#1D1D1D', outline='')            # box track
        canvas.create_rectangle(218.0,  self.y + 88, 1440.0, self.y + 88.5, fill='#FFC16C', outline='')    # orange middle
        canvas.create_rectangle(218.0, self.y, 1440.0, self.y+5, fill=self.color, outline='')              # track3 top bar

        # LEFT BOX
        canvas.create_rectangle(0.0, self.y, 206.0, self.y+171, fill='#292929', outline='')
        canvas.create_rectangle(0.0, self.y+26, 206.0, self.y+171, fill='#1D1D1D', outline='')           # track 3 left bar
        canvas.create_rectangle(0.0, self.y, 7.0, self.y+26, fill=self.color, outline='')                      #

        # BUTTONS
        self.buttons = []

        # GAIN
        self.image_slider_0 = PhotoImage(file=relative_to_assets('slider_0.png'))
        self.image_slider_25 = PhotoImage(file=relative_to_assets('slider_25.png'))
        self.image_slider_50 = PhotoImage(file=relative_to_assets('slider_50.png'))
        self.image_slider_75 = PhotoImage(file=relative_to_assets('slider_75.png'))
        self.image_slider_100 = PhotoImage(file=relative_to_assets('slider_100.png'))
        self.image_slider_L25 = PhotoImage(file=relative_to_assets('slider_-25.png'))
        self.image_slider_L50 = PhotoImage(file=relative_to_assets('slider_-50.png'))
        self.image_slider_L75 = PhotoImage(file=relative_to_assets('slider_-75.png'))
        self.image_slider_L100 = PhotoImage(file=relative_to_assets('slider_-100.png'))
        self.button_gain_0 = Button(image=self.image_slider_0, borderwidth=0, highlightthickness=0,command=lambda: self.change_gain(), relief='flat')
        self.button_gain_0.place(x=26.0, y=self.y + 64, width=64.0, height=64.0)
        self.button_gain_25 = Button(image=self.image_slider_25, borderwidth=0, highlightthickness=0,command=lambda: self.change_gain(), relief='flat')
        self.button_gain_25.place(x=26.0, y=self.y + 64, width=64.0, height=64.0)
        self.button_gain_50 = Button(image=self.image_slider_50, borderwidth=0, highlightthickness=0,command=lambda: self.change_gain(), relief='flat')
        self.button_gain_50.place(x=26.0, y=self.y + 64, width=64.0, height=64.0)
        self.button_gain_75 = Button(image=self.image_slider_75, borderwidth=0, highlightthickness=0,command=lambda: self.change_gain(), relief='flat')
        self.button_gain_75.place(x=26.0, y=self.y + 64, width=64.0, height=64.0)
        self.button_gain_100 = Button(image=self.image_slider_100, borderwidth=0, highlightthickness=0,command=lambda: self.change_gain(), relief='flat')
        self.button_gain_100.place(x=26.0, y=self.y + 64, width=64.0, height=64.0)
        self.button_gain_L25 = Button(image=self.image_slider_L25, borderwidth=0, highlightthickness=0,command=lambda: self.change_gain(), relief='flat')
        self.button_gain_L25.place(x=26.0, y=self.y + 64, width=64.0, height=64.0)
        self.button_gain_L50 = Button(image=self.image_slider_L50, borderwidth=0, highlightthickness=0,command=lambda: self.change_gain(), relief='flat')
        self.button_gain_L50.place(x=26.0, y=self.y + 64, width=64.0, height=64.0)
        self.button_gain_L75 = Button(image=self.image_slider_L75, borderwidth=0, highlightthickness=0,command=lambda: self.change_gain(), relief='flat')
        self.button_gain_L75.place(x=26.0, y=self.y + 64, width=64.0, height=64.0)
        self.button_gain_L100 = Button(image=self.image_slider_L100, borderwidth=0, highlightthickness=0,command=lambda: self.change_gain(), relief='flat')
        self.button_gain_L100.place(x=26.0, y=self.y + 64, width=64.0, height=64.0)
        self.button_gain_0.tkraise()
        canvas.create_text(48.0, self.y+53, anchor='nw', text='Gain', fill='#FFFFFF', font=('Roboto Light', 10 * -1))
        canvas.create_text(41.0, self.y+138, anchor='nw', text='+0 Db', fill='#FFFFFF', font=('Roboto', 12 * -1))

        # PAN
        self.button_pan_0 = Button(image=self.image_slider_0, borderwidth=0, highlightthickness=0,command=lambda: self.change_pan(), relief='flat')
        self.button_pan_0.place(x=116.0, y=self.y + 64, width=64.0, height=64.0)
        self.button_pan_25 = Button(image=self.image_slider_25, borderwidth=0, highlightthickness=0,command=lambda: self.change_pan(), relief='flat')
        self.button_pan_25.place(x=116.0, y=self.y + 64, width=64.0, height=64.0)
        self.button_pan_50 = Button(image=self.image_slider_50, borderwidth=0, highlightthickness=0,command=lambda: self.change_pan(), relief='flat')
        self.button_pan_50.place(x=116.0, y=self.y + 64, width=64.0, height=64.0)
        self.button_pan_75 = Button(image=self.image_slider_75, borderwidth=0, highlightthickness=0,command=lambda: self.change_pan(), relief='flat')
        self.button_pan_75.place(x=116.0, y=self.y + 64, width=64.0, height=64.0)
        self.button_pan_100 = Button(image=self.image_slider_100, borderwidth=0, highlightthickness=0, command=lambda: self.change_pan(), relief='flat')
        self.button_pan_100.place(x=116.0, y=self.y + 64, width=64.0, height=64.0)
        self.button_pan_L25 = Button(image=self.image_slider_L25, borderwidth=0, highlightthickness=0,command=lambda: self.change_pan(), relief='flat')
        self.button_pan_L25.place(x=116.0, y=self.y + 64, width=64.0, height=64.0)
        self.button_pan_L50 = Button(image=self.image_slider_L50, borderwidth=0, highlightthickness=0,command=lambda: self.change_pan(), relief='flat')
        self.button_pan_L50.place(x=116.0, y=self.y + 64, width=64.0, height=64.0)
        self.button_pan_L75 = Button(image=self.image_slider_L75, borderwidth=0, highlightthickness=0,command=lambda: self.change_pan(), relief='flat')
        self.button_pan_L75.place(x=116.0, y=self.y + 64, width=64.0, height=64.0)
        self.button_pan_L100 = Button(image=self.image_slider_L100, borderwidth=0, highlightthickness=0,command=lambda: self.change_pan(), relief='flat')
        self.button_pan_L100.place(x=116.0, y=self.y + 64, width=64.0, height=64.0)
        self.button_pan_0.tkraise()
        canvas.create_text(140.0, self.y+53, anchor='nw', text='Pan', fill='#FFFFFF', font=('Roboto Light', 10 * -1))
        canvas.create_text(140.0, self.y + 138, anchor='nw', text='Mid', fill='#FFFFFF', font=('Roboto', 12 * -1))

        # SOLO
        self.image_solo = PhotoImage(file=relative_to_assets('solo.png'))
        self.image_solo_active = PhotoImage(file=relative_to_assets('solo_active.png'))
        self.button_solo_active = Button(image=self.image_solo_active, borderwidth=0, highlightthickness=0,command=lambda: self.toggle_solo(), relief='flat')
        self.button_solo_active.place(x=179.0, y=self.y + 6, width=15.0, height=15.0)
        self.button_solo = Button(image=self.image_solo, borderwidth=0, highlightthickness=0, command=lambda: self.toggle_solo(), relief='flat')
        self.button_solo.place(x=179.0, y=self.y+6, width=15.0, height=15.0)

        # MUTE
        self.image_mute = PhotoImage(file=relative_to_assets('mute.png'))
        self.image_mute_active = PhotoImage(file=relative_to_assets('mute_active.png'))
        self.button_mute_active = Button(image=self.image_mute_active, borderwidth=0, highlightthickness=0,command=lambda: self.toggle_mute(), relief='flat')
        self.button_mute_active.place(x=164.0, y=self.y + 6, width=15.0, height=15.0)
        self.button_mute = Button(image=self.image_mute, borderwidth=0, highlightthickness=0, command=lambda: self.toggle_mute(), relief='flat')
        self.button_mute.place(x=164.0, y=self.y+6, width=15.0, height=15.0)

        # TRACK TEXT 1
        self.button_select = Button( borderwidth=0, highlightthickness=0, background="#292929",command=lambda: self.select_track(), relief='flat')
        self.button_select.place(x=43,y=self.y+7, width=120, height = 15)
        canvas.create_text(43.0, self.y + 7, anchor='nw', text='Track '+str(self.ID), fill='#5B5B5B', font=('Roboto', 12 * -1))

        # DELETE TRACK 1
        self.image_delete = PhotoImage(file=relative_to_assets('delete.png'))
        self.button_delete = Button(image=self.image_delete, borderwidth=0, highlightthickness=0, command=lambda: self.delete_track(), relief='flat')
        self.button_delete.place(x=14.0, y=self.y+9.0, width=10.0, height=10.0)


        self.buttons_bar = [self.button_delete,self.button_mute,self.button_solo,self.button_mute_active,self.button_solo_active]
        self.buttons_gain = [self.button_gain_0, self.button_gain_25,self.button_gain_50, self.button_gain_75, self.button_gain_100,
                            self.button_gain_L100,self.button_gain_L75,self.button_gain_L50,self.button_gain_L25, ]
        self.buttons_pan = [self.button_pan_0, self.button_pan_25, self.button_pan_50,self.button_pan_75, self.button_pan_100,
                             self.button_pan_L100,self.button_pan_L75,self.button_pan_L50,self.button_pan_L25, ]

        self.intervall = 0


    """ EVERYTHING RECORDING """
    def start_recording(self):
        """ microphone.py handles everything from recording to saving as wav """
        self.mic.start_record("track"+str(self.ID)+".wav")

    def animate_recording(self):

            # draw recording line
            volume = self.mic.mic_volume

            if self.context.RECORDING:
                self.intervall += 1

                # end reached? reset!
                if self.intervall > 1200:
                    self.intervall = 0
                    # TRACK BOX
                    self.canvas.create_rectangle(218.0, self.y + 5, 1440.0, self.y + 171, fill='#1D1D1D', outline='')       # box track
                    self.canvas.create_rectangle(218.0, self.y + 88, 1440.0, self.y + 88.5, fill='#FFC16C', outline='')     # orange middle
                    self.canvas.create_rectangle(218.0, self.y, 1440.0, self.y + 5, fill=self.color, outline='')            # track3 top bar

                # draw recording animation
                self.canvas.create_rectangle(float( 217 + self.intervall), max(self.y+88 - float(volume // 40), self.y), float(217 + self.intervall), self.y+88, fill="#9B7347", outline="")
                self.canvas.create_rectangle(float(217 + self.intervall), min(self.y+88 + float(volume // 40), self.y+171), float(217 + self.intervall), self.y+88, fill="#9B7347", outline="")

            else:
                self.intervall = 0.01  # reset


    """ EVERYTHING UI """
    def select_track(self):
        """ Highlights the selected track via change color """

        self.SELECTED = not self.SELECTED
        if self.SELECTED:

            for button in self.buttons_bar:
               button["bg"] = "#232323"
            for button in self.buttons_pan:
                button["bg"] = "#151515"
            for button in self.buttons_gain:
                button["bg"] = "#151515"

            # TRACK BOX
            #self.canvas.create_rectangle(218.0, self.y + 5, 1440.0, self.y + 171, fill='#1D1D1D', outline='')  # box track
            #self.canvas.create_rectangle(218.0, self.y + 88, 1440.0, self.y + 88.5, fill='#FFC16C',outline='')  # orange middle
            #self.canvas.create_rectangle(218.0, self.y, 1440.0, self.y + 5, fill=self.color, outline='')  # track3 top bar

            # LEFT BOX
            self.canvas.create_rectangle(0.0, self.y, 206.0, self.y + 171, fill="#232323", outline='')
            self.canvas.create_rectangle(0.0, self.y + 26, 206.0, self.y + 171, fill='#151515',outline='')  # track 3 left bar
            self.canvas.create_rectangle(0.0, self.y, 7.0, self.y + 26, fill=self.color, outline='')  #
        else:

            for button in self.buttons_bar:
                button["bg"] = "#292929"
            for button in self.buttons_pan:
                button["bg"] = "#1D1D1D"
            for button in self.buttons_gain:
                button["bg"] = "#1D1D1D"
            # TRACK BOX
            self.canvas.create_rectangle(218.0, self.y + 5, 1440.0, self.y + 171, fill='#1D1D1D', outline='')  # box track
            self.canvas.create_rectangle(218.0, self.y + 88, 1440.0, self.y + 88.5, fill='#FFC16C', outline='')  # orange middle
            self.canvas.create_rectangle(218.0, self.y, 1440.0, self.y + 5, fill=self.color, outline='')  # track3 top bar

            # LEFT BOX
            self.canvas.create_rectangle(0.0, self.y, 206.0, self.y + 171, fill='#292929', outline='')
            self.canvas.create_rectangle(0.0, self.y + 26, 206.0, self.y + 171, fill='#1D1D1D', outline='')  # track 3 left bar
            self.canvas.create_rectangle(0.0, self.y, 7.0, self.y + 26, fill=self.color, outline='')

    def delete_track(self):
        """ Deletes every element and redraws surface black """
        for button in self.buttons_bar:
            button.destroy()
        for button in self.buttons_gain:
            button.destroy()
        for button in self.buttons_pan:
            button.destroy()
        self.canvas.create_rectangle(0, self.y, 1440, self.y + 172, fill="#111111", outline="")  # BOX
        self.context.TRACKS.remove(self)


    """ AUDIO OPTIONS """
    def change_pan(self):
        self.PAN = (self.PAN + 1) % 9
        self.buttons_pan[self.PAN].tkraise()
        song = AudioSegment.from_wav("recordings/raw/track" + str(self.ID) + ".wav")

        self.canvas.create_rectangle(120, self.y+138, 180, self.y + 150, fill="#1D1D1D", outline="")  # overdraw old text
        if self.PAN < 5:    # right side
            print("WAV PAN: ", (+self.PAN*2 /10))
            panned = song.pan(+self.PAN*2 /10)
            self.canvas.create_text(140.0, self.y + 138, anchor='nw', text=str((+self.PAN*2 /10)), fill='#FFFFFF', font=('Roboto', 12 * -1))
        else:
            print("WAV PAN: ", (-9 + self.PAN) / 5)
            panned = song.pan((-9 + self.PAN) / 5)
            self.canvas.create_text(140.0, self.y + 138, anchor='nw', text=str((-9 + self.PAN) / 5), fill='#FFFFFF', font=('Roboto', 12 * -1))

        panned.export("recordings/edited/track" + str(self.ID) + ".wav", "wav")

    def change_gain(self):
        """ Changes gain of RAW editing
            TODO: Pick editing but dont reapply gain """

        self.GAIN = (self.GAIN + 1) % 9
        self.buttons_gain[self.GAIN].tkraise()
        song = AudioSegment.from_wav("recordings/raw/track" + str(self.ID) + ".wav")
        self.canvas.create_rectangle(40, self.y + 138, 80, self.y + 150, fill="#1D1D1D",outline="")  # overdraw old text

        if self.GAIN > 4:   # negative side
            print("WAV GAIN: ", 2**abs((-8+self.GAIN)) * -1)
            gained = song.apply_gain(-9+self.GAIN)
            self.canvas.create_text(41.0, self.y+138, anchor='nw', text=str(-9+self.GAIN) + ' Db', fill='#FFFFFF', font=('Roboto', 12 * -1))
        elif self.GAIN > 0:  # right side
            print("WAV GAIN: ", 2**(self.GAIN-1))
            gained = song.apply_gain(2**(self.GAIN-1))
            self.canvas.create_text(41.0, self.y+138, anchor='nw', text='+'+str(2**(self.GAIN-1)) + ' Db', fill='#FFFFFF', font=('Roboto', 12 * -1))
        else:   # gain = 0
            print("WAV GAIN: ", self.GAIN)
            gained = song.apply_gain(0)
            self.canvas.create_text(41.0, self.y + 138, anchor='nw', text='+' + str(self.GAIN) + ' Db',
                                    fill='#FFFFFF', font=('Roboto', 12 * -1))
        gained.export("recordings/edited/track" + str(self.ID) + ".wav", "wav")

    def toggle_mute(self):
        self.MUTE = not self.MUTE
        if self.MUTE:
            self.button_mute_active.tkraise()
            self.canvas.create_rectangle(218.0, self.y, 1440.0, self.y+5, fill="#1D1D1D", outline="")
        else:
            self.button_mute.tkraise()
            self.canvas.create_rectangle(218.0, self.y, 1440.0, self.y+5, fill=self.color, outline="")
    def set_mute(self, muted):
        self.MUTE = not muted
        self.toggle_mute()
    def toggle_solo(self):
        self.SOLO = not self.SOLO
        if self.SOLO:
            self.button_solo_active.tkraise()
            self.context.UPDATEUI_SOLO = True
        else:
            self.button_solo.tkraise()
            self.context.UPDATEUI_SOLO = True


    def save(self, path=""):
        imported_file = AudioSegment.from_wav(self.filename)
        imported_file.export("recordings/raw/track" + str(self.ID) + ".wav", format="wav")
        print("[TRACK] Track saved as " + "recordings/raw/track" + str(self.ID) + ".wav")