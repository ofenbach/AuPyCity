from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./bottom_bar/")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()
window.geometry("1440x1000")
window.configure(bg = "#111111")

canvas = Canvas(window, bg = "#111111", height = 1000, width = 1440, bd = 0, highlightthickness = 0, relief = "ridge")
canvas.place(x = 0, y = 0)
canvas.create_rectangle(0.0,917.0,1440.0,1000.0,fill="#1D1D1D", outline="")

image_settings = PhotoImage(file=relative_to_assets("settings.png"))
button_settings = Button(image=image_settings,bg="#1D1D1D",borderwidth=0, highlightthickness=0,command=lambda: print("button_1 clicked"),relief="flat")
button_settings.place(x=1351.0,y=932.0,width=33.0,height=53.0)

image_help = PhotoImage(file=relative_to_assets("help.png"))
button_help = Button(image=image_help, bg="#1D1D1D",borderwidth=0,highlightthickness=0,command=lambda: print("button_2 clicked"), relief="flat")
button_help.place(x=1230.0, y=932.0,width=32.0,height=53.0)

image_donate = PhotoImage(file=relative_to_assets("donate.png"))
button_donate = Button(image=image_donate,bg="#1D1D1D",borderwidth=0,highlightthickness=0,command=lambda: print("button_3 clicked"),relief="flat")
button_donate.place(x=1170.0,y=932.0,  width=32.0,height=53.0)

canvas.create_rectangle( 1295.0,936.0, 1295.0000019670128,981.0,fill="#2F2F2F",outline="")
canvas.create_rectangle(319.0000000000001,936.0,319.00000196701296,981.0,fill="#2F2F2F",outline="")

image_noisefilter = PhotoImage(file=relative_to_assets("noisefilter.png"))
button_noisefilter = Button(image=image_noisefilter,bg="#1D1D1D",borderwidth=0,highlightthickness=0,command=lambda: print("button_4 clicked"),relief="flat")
button_noisefilter.place( x=634.0000000000001,y=938.0,width=46.0,height=49.0)

image_compressor = PhotoImage(file=relative_to_assets("compressor.png"))
button_compressor = Button(image=image_compressor,bg="#1D1D1D",borderwidth=0,highlightthickness=0,command=lambda: print("button_5 clicked"),relief="flat")
button_compressor.place(x=543.0000000000001,y=938.0,width=50.0,height=49.0)

image_normalizer = PhotoImage(file=relative_to_assets("normalizer.png"))
button_normalizer = Button(image=image_normalizer, bg="#1D1D1D", borderwidth=0,highlightthickness=0, command=lambda: print("button_6 clicked"),relief="flat")
button_normalizer.place(x=458.0000000000001, y=938.0, width=44.0, height=49.0)

image_equalizer = PhotoImage( file=relative_to_assets("equalizer.png"))
button_equalizer = Button(image=image_equalizer, bg="#1D1D1D", borderwidth=0, highlightthickness=0,command=lambda: print("button_7 clicked"),relief="flat")
button_equalizer.place( x=374.0000000000001, y=938.0,  width=37.0,  height=49.0)

canvas.create_rectangle(735.0000000000001,936.0, 735.000001967013,981.0,fill="#2F2F2F",outline="")

image_stereo = PhotoImage(file=relative_to_assets("stereo.png"))
button_stereo = Button(image=image_stereo, bg="#1D1D1D",borderwidth=0,highlightthickness=0,command=lambda: print("button_8 clicked"),relief="flat")
button_stereo.place(x=213.0000000000001,y=916.0,width=68.0,height=83.0)

image_sampling441 = PhotoImage(file=relative_to_assets("sampling441.png"))
button_sampling441 = Button(image=image_sampling441,bg="#1D1D1D",borderwidth=0,highlightthickness=0,command=lambda: print("button_9 clicked"),relief="flat")
button_sampling441.place(x=125.00000000000011,y=917.0,width=68.0,height=83.0)

image_bitdepth32 = PhotoImage(file=relative_to_assets("bitdepth32.png"))
button_bitdepth32 = Button(image=image_bitdepth32,bg="#1D1D1D", borderwidth=0, highlightthickness=0,command=lambda: print("button_10 clicked"),relief="flat")
button_bitdepth32.place(x=37.000000000000114,y=916.0, width=68.0,height=84.0)


window.resizable(False, False)
window.mainloop()
