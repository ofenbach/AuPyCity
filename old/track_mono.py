import time
from pathlib import Path
from tkinter import Tk, Canvas, Text, Button
from PIL import ImageTk
from PIL import Image

# PATH STUFF
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


class MonoTrack:

    def __init__(self, window,canvas,context):
        self.window = window
        self.context = context
        self.canvas = canvas

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
        self.y = 32+ 200*self.ID
        colors = ["#02ECFE", "#9F40F0", "#0FE511", "#FF5AD4", "#02ECFE"]
        self.color = colors[self.ID]
        self.SELECTED = False

        # AUDIO
        self.PAN = 0
        self.GAIN = 0
        self.MUTE = False
        self.SOLO = False

        # LOAD IMAGES
        self.img_slider = ImageTk.PhotoImage(Image.open("icons/work_frame/slider.png").resize((120, 120)))
        self.img_sliderL = ImageTk.PhotoImage(Image.open("icons/work_frame/sliderL.png").resize((120, 120)))
        self.img_sliderR = ImageTk.PhotoImage(Image.open("icons/work_frame/sliderR.png").resize((120, 120)))
        self.img_slider50L = ImageTk.PhotoImage(Image.open("icons/work_frame/slider50L.png").resize((120, 120)))
        self.img_slider50R = ImageTk.PhotoImage(Image.open("icons/work_frame/slider50R.png").resize((120, 120)))
        self.img_solo = ImageTk.PhotoImage(Image.open("icons/work_frame/solo.png").resize((30, 30)))
        self.img_mute = ImageTk.PhotoImage(Image.open("icons/work_frame/mute.png").resize((30, 30)))
        self.img_x =ImageTk.PhotoImage(Image.open("icons/work_frame/x.png").resize((8, 8)))

        # BUTTONS
        self.buttons = []
        self.button_trackselection = Button(text="Track" + str(self.ID),fg="#5B5B5B",bg="#292929", font=("Roboto", 12 * -1),borderwidth=0, highlightthickness=0, relief="flat",command=lambda: self.select_track())
        self.button_trackselection.place(x=self.x + 7, y=self.y + 133, width=199, height=26)
        self.button_pan = Button(image=self.img_slider, bg="#1D1D1D",borderwidth=0, highlightthickness=0, relief="flat",command=lambda: self.change_pan())
        self.button_pan = Button(image=self.img_slider, borderwidth=0, bg="#1D1D1D", highlightthickness=0,relief="flat", command=lambda: self.change_pan())
        self.button_panR = Button(image=self.img_sliderR, borderwidth=0, bg="#1D1D1D", highlightthickness=0,relief="flat", command=lambda: self.change_pan())
        self.button_panL = Button(image=self.img_sliderL, borderwidth=0, bg="#1D1D1D", highlightthickness=0,relief="flat", command=lambda: self.change_pan())
        self.button_pan50R = Button(image=self.img_slider50R, borderwidth=0, bg="#1D1D1D", highlightthickness=0, relief="flat", command=lambda: self.change_pan())
        self.button_pan50L = Button(image=self.img_slider50L, borderwidth=0, bg="#1D1D1D", highlightthickness=0,relief="flat", command=lambda: self.change_pan())
        self.button_gain = Button(image=self.img_slider, borderwidth=0, bg="#1D1D1D",highlightthickness=0, relief="flat",command=lambda: self.change_gain())
        self.button_gainR = Button(image=self.img_sliderR, borderwidth=0, bg="#1D1D1D", highlightthickness=0,relief="flat", command=lambda: self.change_gain())
        self.button_gainL = Button(image=self.img_sliderL, borderwidth=0, bg="#1D1D1D", highlightthickness=0,relief="flat", command=lambda: self.change_gain())
        self.button_gain50R = Button(image=self.img_slider50R, borderwidth=0, bg="#1D1D1D", highlightthickness=0,relief="flat", command=lambda: self.change_gain())
        self.button_gain50L = Button(image=self.img_slider50L, borderwidth=0, bg="#1D1D1D", highlightthickness=0,relief="flat", command=lambda: self.change_gain())
        self.button_solo = Button(image=self.img_solo, borderwidth=0, highlightthickness=0, relief="flat",command=lambda: self.toggle_solo())
        self.button_mute = Button(image=self.img_mute, borderwidth=0, highlightthickness=0, relief="flat",command=lambda: self.toggle_mute())
        self.button_x = Button(image=self.img_x, borderwidth=0, highlightthickness=0, relief="flat",command=self.delete_track)
        self.buttons.extend([self.button_x,self.button_mute,self.button_solo,self.button_gain,self.button_pan, self.button_trackselection])

    def draw_track(self, window, canvas):
        self.canvas = canvas

        # TRACK 0 MAIN
        self.canvas.create_rectangle(self.x+218, self.y+139, 2000, self.y+309, fill="#1D1D1D", outline="")  # BOX
        self.canvas.create_rectangle(self.x+218, self.y+221, 2000, self.y+223, fill="#9B7347", outline="")  # ORANGE MIDDLE
        self.canvas.create_rectangle(self.x+218, self.y+133, 2000, self.y+139, fill=self.color, outline="")  # BLUE TOP BAR

        # Track 0 LEFT BOX
        self.canvas.create_rectangle(self.x, self.y+133, self.x + 206, self.y+309, fill="#1D1D1D", outline="")   # LEFT SETTINGS BOX
        self.button_trackselection.place(x=self.x+7,y=self.y+133, width=180, height=26)
        self.canvas.create_rectangle(self.x+7, self.y+133, self.x + 206, self.y+159, fill="#292929", outline="")   # GRAY BAR
        self.canvas.create_rectangle(self.x, self.y+133, self.x + 7,   self.y+159, fill=self.color,outline="")                     # BLUE BAR
        self.button_solo.place(x=181, y=self.y+139, width=16, height=16)
        self.button_mute.place(x=160, y=self.y+139, width=16, height=16)
        self.button_x.place(x=14, y=self.y+142, width=8, height=8)

        # PAN
        self.canvas.create_text(140, self.y+175, anchor="nw", text="Pan", fill="#A7A7A7", font=("Roboto", 12 * -1))
        self.button_pan.place(x=125, y=self.y + 201, width=64, height=64)
        self.button_pan50L.place(x=125, y=self.y + 201, width=64, height=64)
        self.button_pan50R.place(x=125, y=self.y + 201, width=64, height=64)
        self.button_panL.place(x=125, y=self.y + 201, width=64, height=64)
        self.button_panR.place(x=125, y=self.y + 201, width=64, height=64)
        self.canvas.create_rectangle(120, self.y+200, 200, self.y+290, fill="#1D1D1D", outline="")  # BOX LEFT

        # GAIN
        self.canvas.create_text(45, self.y+175, anchor="nw", text="Gain", fill="#A7A7A7", font=("Roboto", 12 * -1))
        self.button_gain.place(x=32, y=self.y + 201, width=64, height=64)
        self.button_gain50L.place(x=32, y=self.y + 201, width=64, height=64)
        self.button_gain50R.place(x=32, y=self.y + 201, width=64, height=64)
        self.button_gainL.place(x=32, y=self.y + 201, width=64, height=64)
        self.button_gainR.place(x=32, y=self.y + 201, width=64, height=64)

        # if re recorded raise buttons to make sure they are visible
        self.button_gain.tkraise()
        self.button_pan.tkraise()
        self.button_x.tkraise()

    def start_recording(self):

        while self.context.RECORDING:

            pass

        # save track

    def delete_track(self):
        for button in self.buttons:
            button.destroy()
        self.canvas.create_rectangle(0, self.y + 130, 1280 * 4, self.y + 320, fill="#111111", outline="")  # BOX
        self.context.TRACKS.remove(self)

    def change_pan(self):
        self.PAN += 0.5
        if self.PAN == 1.5:
            self.PAN = -1
            self.button_panL.tkraise()
        if self.PAN == -0.5:
            self.button_pan50L.tkraise()
        if self.PAN == 0:
            self.button_pan.tkraise()
        if self.PAN == +0.5:
            self.button_pan50R.tkraise()
        if self.PAN == +1.0:
            self.button_panR.tkraise()

    def change_gain(self):
        self.GAIN += 0.5
        if self.GAIN == 1.5:
            self.GAIN = -1
            self.button_gainL.tkraise()
        if self.GAIN == -0.5:
            self.button_gain50L.tkraise()
        if self.GAIN == 0:
            self.button_gain.tkraise()
        if self.GAIN == +0.5:
            self.button_gain50R.tkraise()
        if self.GAIN == +1.0:
            self.button_gainR.tkraise()

    def toggle_mute(self):
        self.MUTE = not self.MUTE
        if self.MUTE:
            self.canvas.create_rectangle(self.x+218, self.y+133, self.x+2000.0, self.y+139, fill="#1D1D1D", outline="")
        else:
            self.canvas.create_rectangle(self.x+218, self.y+133, self.x+2000.0, self.y+139, fill=self.color, outline="")
    def toggle_solo(self):
        self.SOLO = not self.SOLO

    def select_track(self):
        self.SELECTED = not self.SELECTED
        if self.SELECTED:
            self.button_trackselection["bg"] = "#232323"
            self.button_pan["bg"] = "#151515"
            self.button_panR["bg"] = "#151515"
            self.button_panL["bg"] = "#151515"
            self.button_pan50R["bg"] = "#151515"
            self.button_pan50L["bg"] = "#151515"
            self.button_gainR["bg"] = "#151515"
            self.button_gain["bg"] = "#151515"
            self.button_gainL["bg"] = "#151515"
            self.button_gain50R["bg"] = "#151515"
            self.button_gain50L["bg"] = "#151515"
            self.canvas.create_rectangle(self.x+7, self.y + 133, self.x + 206, self.y + 159, fill="#232323",outline="")  # GRAY BAR
            self.canvas.create_rectangle(self.x, self.y + 159, self.x + 206, self.y + 309, fill="#151515", outline="")
            self.canvas.create_text(45, self.y + 175, anchor="nw", text="Gain", fill="#A7A7A7",font=("Roboto", 12 * -1))
            self.canvas.create_text(140, self.y + 175, anchor="nw", text="Pan", fill="#A7A7A7",font=("Roboto", 12 * -1))
        else:
            self.button_trackselection["bg"] = "#292929"
            self.button_pan["bg"] = "#1D1D1D"
            self.button_panR["bg"] = "#1D1D1D"
            self.button_panL["bg"] = "#1D1D1D"
            self.button_pan50R["bg"] = "#1D1D1D"
            self.button_pan50L["bg"] = "#1D1D1D"
            self.button_gain["bg"] = "#1D1D1D"
            self.button_gainR["bg"] = "#1D1D1D"
            self.button_gainL["bg"] = "#1D1D1D"
            self.button_gain50R["bg"] = "#1D1D1D"
            self.button_gain50L["bg"] = "#1D1D1D"
            self.canvas.create_rectangle(self.x+7, self.y + 133, self.x + 206, self.y + 159, fill="#292929",outline="")  # GRAY BAR
            self.canvas.create_rectangle(self.x, self.y + 159, self.x + 206, self.y + 309, fill="#1D1D1D", outline="")
            self.canvas.create_text(45, self.y + 175, anchor="nw", text="Gain", fill="#A7A7A7",font=("Roboto", 12 * -1))
            self.canvas.create_text(140, self.y + 175, anchor="nw", text="Pan", fill="#A7A7A7",font=("Roboto", 12 * -1))