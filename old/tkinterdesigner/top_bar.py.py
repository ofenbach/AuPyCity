from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("top_bar/")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()
window.geometry("1440x1000")
window.configure(bg = "#111111")


canvas = Canvas(window, bg = "#111111", height = 96+23, width = 1440, bd = 0, highlightthickness = 0, relief = "ridge")
canvas.place(x = 0, y = 0)

canvas.create_rectangle( 0.0,95.0,1440.0,117.0,fill="#292929",outline="")   # backbox

# cutter line
image_cutter = PhotoImage(file=relative_to_assets("time_line.png"))
button_cutter = Button(image=image_cutter,borderwidth=0,highlightthickness=0,command=lambda: print("button_1 clicked"),relief="flat")
button_cutter.place(x=218.0, y=95.0, width=1280.0, height=22.0)

# time text
canvas.create_text(68.0,100.0,anchor="nw",text="00:00:00.000",fill="#FFFFFF", font=("Roboto", 12 * -1))
canvas.create_rectangle(0.0,23.0,1440.0,95.0,fill="#1D1D1D",outline="")

# fullscreen
image_fullscreen = PhotoImage(file=relative_to_assets("fullscreen.png"))
button_fullscreen = Button(image=image_fullscreen,borderwidth=0,highlightthickness=0,bg="#1D1D1D",command=lambda: print("button_2 clicked"),relief="flat")
button_fullscreen.place(x=1390.0,y=46.0,width=27.0,height=27.0)

# cutter
canvas.create_rectangle(1367.0,37.0,1367.0000019670128,82.0,fill="#2F2F2F",outline="")

# import
image_import = PhotoImage(file=relative_to_assets("import.png"))
button_import = Button(image=image_import,bg="#1D1D1D", borderwidth=0,highlightthickness=0,command=lambda: print("button_3 clicked"),relief="flat")
button_import.place(x=1272.0,y=38.0, width=28.0,height=42.0)

# export
image_export = PhotoImage(file=relative_to_assets("export.png"))
button_export = Button(image=image_export,bg="#1D1D1D",borderwidth=0,highlightthickness=0,command=lambda: print("button_4 clicked"),relief="flat")
button_export.place(x=1316.0,y=38.0,width=28.0,height=42.0)

# preview
image_preview = PhotoImage(file=relative_to_assets("preview.png"))
button_preview = Button(image=image_preview,bg="#1D1D1D",borderwidth=0,highlightthickness=0, command=lambda: print("button_5 clicked"),relief="flat")
button_preview.place(x=1209.0,y=38.0, width=31.0,height=42.0)

# cutter
canvas.create_rectangle(1012.0,37.0,1012.0000019670128,82.0,fill="#2F2F2F",outline="")

image_paint = PhotoImage(file=relative_to_assets("paint.png"))
button_paint = Button(image=image_paint,borderwidth=0,bg="#1D1D1D",highlightthickness=0,command=lambda: print("button_6 clicked"),relief="flat")
button_paint.place(x=954.0,y=36.0, width=18.0,height=18.0)

image_zoomout = PhotoImage(file=relative_to_assets("zoom_out.png"))
button_zoomout = Button(image=image_zoomout,bg="#1D1D1D",borderwidth=0,highlightthickness=0, command=lambda: print("button_7 clicked"),relief="flat")
button_zoomout.place(x=954.0,y=66.0,width=18.0, height=18.0)

image_zoomin = PhotoImage(file=relative_to_assets("zoom.png"))
button_zoomin = Button(image=image_zoomin,bg="#1D1D1D",borderwidth=0,highlightthickness=0,command=lambda: print("button_8 clicked"),relief="flat")
button_zoomin.place(x=928.0, y=66.0,width=18.0,height=18.0)

image_reset = PhotoImage(file=relative_to_assets("reset.png"))
button_reset = Button(image=image_reset,bg="#1D1D1D",borderwidth=0,highlightthickness=0,command=lambda: print("button_9 clicked"),relief="flat")
button_reset.place(x=928.0,y=36.0,width=18.0,height=18.0)

image_drag = PhotoImage(file=relative_to_assets("drag.png"))
button_drag = Button(image=image_drag,bg="#1D1D1D",borderwidth=0,highlightthickness=0,command=lambda: print("button_10 clicked"),relief="flat")
button_drag.place(x=902.0,y=66.0,width=18.0,height=18.0)

image_click = PhotoImage(file=relative_to_assets("click.png"))
button_click = Button(image=image_click,bg="#1D1D1D",borderwidth=0,highlightthickness=0,command=lambda: print("button_11 clicked"),relief="flat")
button_click.place(x=876.0,y=66.0,width=18.0,height=18.0)

image_redo = PhotoImage(file=relative_to_assets("redo.png"))
button_redo = Button(image=image_redo, bg="#1D1D1D",borderwidth=0,highlightthickness=0,command=lambda: print("button_12 clicked"),relief="flat")
button_redo.place(x=902.0,y=36.0,width=18.0,height=18.0)

image_undo = PhotoImage(file=relative_to_assets("undo.png"))
button_undo = Button(image=image_undo,bg="#1D1D1D",borderwidth=0,highlightthickness=0,command=lambda: print("button_13 clicked"),relief="flat")
button_undo.place(x=876.0,y=36.0,width=18.0,height=18.0)

image_ear = PhotoImage(file=relative_to_assets("ear.png"))
button_ear = Button(image=image_ear,borderwidth=0,bg="#1D1D1D", highlightthickness=0,command=lambda: print("button_14 clicked"),relief="flat")
button_ear.place(x=842.0,y=36.0,width=18.0,height=18.0)

image_mute = PhotoImage(file=relative_to_assets("mute.png"))
button_mute = Button(image=image_mute,bg="#1D1D1D",borderwidth=0, highlightthickness=0,command=lambda: print("button_15 clicked"),relief="flat")
button_mute.place(x=842.0, y=66.0,width=18.0,height=18.0)

# cutter
canvas.create_rectangle(802.0,37.0,802.0000019670128,82.0,fill="#2F2F2F",outline="")

image_volumespeakerbar = PhotoImage(file=relative_to_assets("volume_speakerbar.png"))
button_speakervolumebar = Button(image=image_volumespeakerbar,bg="#1D1D1D",borderwidth=0,highlightthickness=0,command=lambda: print("button_16 clicked"),relief="flat")
button_speakervolumebar.place(x=603.0,y=52.0,width=119.0,height=14.0)

image_expand = PhotoImage(file=relative_to_assets("expand.png"))
button_expand = Button(image=image_expand,bg="#1D1D1D",borderwidth=0,highlightthickness=0,command=lambda: print("button_17 clicked"),relief="flat")
button_expand.place(x=586.0,y=55.0,width=10.0,height=8.0)

image_speaker = PhotoImage(file=relative_to_assets("speaker.png"))
button_speaker = Button(image=image_speaker,bg="#1D1D1D",borderwidth=0,highlightthickness=0,command=lambda: print("button_18 clicked"),relief="flat")
button_speaker.place(x=567.0, y=50.0, width=18.0, height=18.0)

image_volumebar = PhotoImage( file=relative_to_assets("volumebar.png"))
button_volumebar = Button(image=image_volumebar,bg="#1D1D1D",borderwidth=0,highlightthickness=0,command=lambda: print("button_19 clicked"),relief="flat")
button_volumebar.place(x=424.0,y=54.0,width=119.0,height=7.0)

image_expand = PhotoImage(file=relative_to_assets("expand.png"))
button_expand = Button(image=image_expand,bg="#1D1D1D",borderwidth=0,highlightthickness=0,command=lambda: print("button_20 clicked"), relief="flat")
button_expand.place( x=407.0,y=53.0,width=10.0,height=10.0)

image_mic = PhotoImage(file=relative_to_assets("microphone.png"))
button_mic = Button( image=image_mic,bg="#1D1D1D",borderwidth=0,highlightthickness=0,command=lambda: print("button_21 clicked"),relief="flat")
button_mic.place(x=388.0,y=49.0,width=18.0, height=18.0)

# cutter
canvas.create_rectangle(308.0,37.0,308.00000196701285,82.0,fill="#2F2F2F",outline="")

# record
image_recordactive = PhotoImage(file=relative_to_assets("record_active.png"))
button_recordactive = Button(image=image_recordactive,bg="#1D1D1D", borderwidth=0,highlightthickness=0,command=lambda: print("button_22 clicked"),relief="flat")
button_recordactive.place(x=218.0,y=42.0,width=34.0,height=34.0)

# stop
image_stop = PhotoImage(file=relative_to_assets("stop.png"))
button_stop = Button(image=image_stop,bg="#1D1D1D", borderwidth=0, highlightthickness=0, command=lambda: print("button_23 clicked"), relief="flat")
button_stop.place( x=170.0, y=43.0, width=32.0, height=32.0)

# pause
image_pause = PhotoImage(file=relative_to_assets("pause.png"))
button_pause = Button(image=image_pause,bg="#1D1D1D",borderwidth=0,highlightthickness=0,command=lambda: print("button_24 clicked"),relief="flat")
button_pause.place(x=115.0,y=43.0,width=23.272737503051758,height=32.0)

# play
image_play = PhotoImage(file=relative_to_assets("play.png"))
button_play = Button(image=image_play,bg="#1D1D1D",borderwidth=0,highlightthickness=0,command=lambda: print("button_25 clicked"),relief="flat")
button_play.place( x=56.00006103515625, y=41.0, width=42.62738037109375,height=36.57235336303711)

window.resizable(False, False)
window.mainloop()
