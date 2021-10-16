#!/usr/bin/env python

import threading
from tkinter import PhotoImage, Button, Canvas
from pathlib import Path
from tkinter import filedialog as fd
import sounddevice as sd
import soundfile as sf
from pydub import AudioSegment
from pydub.playback import play


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./tkinterdesigner/top_bar/")
def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


class TopBarUI:

    def __init__(self, window, main_canvas, context):
        self.window = window
        self.context = context

        canvas = Canvas(window, bg="#111111", height=96 + 23, width=1440, bd=0, highlightthickness=0, relief="ridge")
        canvas.place(x=0, y=0)
        self.canvas = canvas

        canvas.create_rectangle(0.0, 95.0, 1440.0, 117.0, fill="#292929", outline="")  # backbox

        # time line
        self.image_timeline = PhotoImage(file=relative_to_assets("time_line.png"))
        self.button_timeline = Button(image=self.image_timeline, borderwidth=0, highlightthickness=0,command=lambda: print("button_1 clicked"), relief="flat")
        self.button_timeline.place(x=218.0, y=95.0, width=1280.0, height=22.0)

        # time text
        canvas.create_text(68.0, 100.0, anchor="nw", text="00:00:00.000", fill="#FFFFFF", font=("Roboto", 12 * -1))
        canvas.create_rectangle(0.0, 23.0, 1440.0, 95.0, fill="#1D1D1D", outline="")

        # fullscreen
        self.image_fullscreen = PhotoImage(file=relative_to_assets("fullscreen.png"))
        self.button_fullscreen = Button(image=self.image_fullscreen, borderwidth=0, highlightthickness=0, bg="#1D1D1D",command=lambda: print("button_2 clicked"), relief="flat")
        self.button_fullscreen.place(x=1390.0, y=46.0, width=27.0, height=27.0)

        # cutter
        canvas.create_rectangle(1367.0, 37.0, 1367.0000019670128, 82.0, fill="#2F2F2F", outline="")

        # import
        self.image_import = PhotoImage(file=relative_to_assets("import.png"))
        self.button_import = Button(image=self.image_import, bg="#1D1D1D", borderwidth=0, highlightthickness=0,command=lambda: self.import_file(), relief="flat")
        self.button_import.place(x=1272.0, y=38.0, width=28.0, height=42.0)

        # export
        self.image_export = PhotoImage(file=relative_to_assets("export.png"))
        self.button_export = Button(image=self.image_export, bg="#1D1D1D", borderwidth=0, highlightthickness=0,command=lambda: self.export(), relief="flat")
        self.button_export.place(x=1316.0, y=38.0, width=28.0, height=42.0)

        # preview
        self.image_preview = PhotoImage(file=relative_to_assets("preview.png"))
        self.button_preview = Button(image=self.image_preview, bg="#1D1D1D", borderwidth=0, highlightthickness=0,
                                command=lambda: self.preview(), relief="flat")
        self.button_preview.place(x=1209.0, y=38.0, width=31.0, height=42.0)

        # cutter
        canvas.create_rectangle(1012.0, 37.0, 1012.0000019670128, 82.0, fill="#2F2F2F", outline="")

        self.image_paint = PhotoImage(file=relative_to_assets("brush.png"))
        self.button_paint = Button(image=self.image_paint, borderwidth=0, bg="#1D1D1D", highlightthickness=0,
                              command=lambda: print("button_6 clicked"), relief="flat")
        self.button_paint.place(x=954.0, y=36.0, width=18.0, height=18.0)

        self.image_zoomout = PhotoImage(file=relative_to_assets("zoom_out.png"))
        self.button_zoomout = Button(image=self.image_zoomout, bg="#1D1D1D", borderwidth=0, highlightthickness=0,
                                command=lambda: print("button_7 clicked"), relief="flat")
        self.button_zoomout.place(x=954.0, y=66.0, width=18.0, height=18.0)

        self.image_zoomin = PhotoImage(file=relative_to_assets("zoom_in.png"))
        self.button_zoomin = Button(image=self.image_zoomin, bg="#1D1D1D", borderwidth=0, highlightthickness=0,
                               command=lambda: print("button_8 clicked"), relief="flat")
        self.button_zoomin.place(x=928.0, y=66.0, width=18.0, height=18.0)

        self.image_reset = PhotoImage(file=relative_to_assets("reset.png"))
        self.button_reset = Button(image=self.image_reset, bg="#1D1D1D", borderwidth=0, highlightthickness=0,
                              command=lambda: print("button_9 clicked"), relief="flat")
        self.button_reset.place(x=928.0, y=36.0, width=18.0, height=18.0)

        self.image_drag = PhotoImage(file=relative_to_assets("drag.png"))
        self.button_drag = Button(image=self.image_drag, bg="#1D1D1D", borderwidth=0, highlightthickness=0,
                             command=lambda: print("button_10 clicked"), relief="flat")
        self.button_drag.place(x=902.0, y=66.0, width=18.0, height=18.0)

        self.image_click = PhotoImage(file=relative_to_assets("cursor.png"))
        self.button_click = Button(image=self.image_click, bg="#1D1D1D", borderwidth=0, highlightthickness=0,
                              command=lambda: print("button_11 clicked"), relief="flat")
        self.button_click.place(x=876.0, y=66.0, width=18.0, height=18.0)

        self.image_redo = PhotoImage(file=relative_to_assets("redo.png"))
        self.button_redo = Button(image=self.image_redo, bg="#1D1D1D", borderwidth=0, highlightthickness=0,
                             command=lambda: print("button_12 clicked"), relief="flat")
        self.button_redo.place(x=902.0, y=36.0, width=18.0, height=18.0)

        self.image_undo = PhotoImage(file=relative_to_assets("undo.png"))
        self.button_undo = Button(image=self.image_undo, bg="#1D1D1D", borderwidth=0, highlightthickness=0,
                             command=lambda: print("button_13 clicked"), relief="flat")
        self.button_undo.place(x=876.0, y=36.0, width=18.0, height=18.0)

        self.image_ear = PhotoImage(file=relative_to_assets("ear.png"))
        self.button_ear = Button(image=self.image_ear, borderwidth=0, bg="#1D1D1D", highlightthickness=0,
                            command=lambda: self.toggle_direct_monitoring(), relief="flat")
        self.button_ear.place(x=842.0, y=36.0, width=18.0, height=18.0)

        self.image_mute = PhotoImage(file=relative_to_assets("mute.png"))
        self.button_mute = Button(image=self.image_mute, bg="#1D1D1D", borderwidth=0, highlightthickness=0,
                             command=lambda: print("button_15 clicked"), relief="flat")
        self.button_mute.place(x=842.0, y=66.0, width=18.0, height=18.0)

        # cutter
        canvas.create_rectangle(802.0, 37.0, 802.0000019670128, 82.0, fill="#2F2F2F", outline="")

        self.image_volumespeakerbar = PhotoImage(file=relative_to_assets("volume_speakerbar.png"))
        self.button_speakervolumebar = Button(image=self.image_volumespeakerbar, bg="#1D1D1D", borderwidth=0,
                                         highlightthickness=0, command=lambda: print("button_16 clicked"),
                                         relief="flat")
        self.button_speakervolumebar.place(x=603.0, y=52.0, width=119.0, height=14.0)

        self.image_expand = PhotoImage(file=relative_to_assets("expand.png"))
        self.button_expand2 = Button(image=self.image_expand, bg="#1D1D1D", borderwidth=0, highlightthickness=0,
                               command=lambda: self.expand_speaker(), relief="flat")
        self.button_expand2.place(x=586.0, y=55.0, width=10.0, height=8.0)

        self.image_speaker = PhotoImage(file=relative_to_assets("speaker.png"))
        self.button_speaker = Button(image=self.image_speaker, bg="#1D1D1D", borderwidth=0, highlightthickness=0,
                                command=lambda: print("button_18 clicked"), relief="flat")
        self.button_speaker.place(x=567.0, y=50.0, width=18.0, height=18.0)

        self.image_volumebar = PhotoImage(file=relative_to_assets("volumebar.png"))
        self.button_volumebar = Button(image=self.image_volumebar, bg="#1D1D1D", borderwidth=0, highlightthickness=0,
                                  command=lambda: print("button_19 clicked"), relief="flat")
        self.button_volumebar.place(x=424.0, y=54.0, width=119.0, height=7.0)

        self.button_expand = Button(image=self.image_expand, bg="#1D1D1D", borderwidth=0, highlightthickness=0,
                               command=lambda: self.expand_mics(), relief="flat")
        self.button_expand.place(x=407.0, y=53.0, width=10.0, height=10.0)

        self.image_mic = PhotoImage(file=relative_to_assets("microphone.png"))
        self.button_mic = Button(image=self.image_mic, bg="#1D1D1D", borderwidth=0, highlightthickness=0,
                            command=lambda: print("button_21 clicked"), relief="flat")
        self.button_mic.place(x=388.0, y=49.0, width=18.0, height=18.0)

        # cutter
        canvas.create_rectangle(308.0, 37.0, 308.00000196701285, 82.0, fill="#2F2F2F", outline="")

        # record
        self.image_recordactive = PhotoImage(file=relative_to_assets("record_active.png"))
        self.button_recordactive = Button(image=self.image_recordactive, bg="#1D1D1D", borderwidth=0, highlightthickness=0,
                                     command=lambda: self.start_recording(), relief="flat")
        self.button_recordactive.place(x=218.0, y=42.0, width=34.0, height=34.0)
        self.image_record_passive = PhotoImage(file=relative_to_assets("record_passive.png"))
        self.button_record_passive = Button(image=self.image_record_passive, bg="#1D1D1D", borderwidth=0,
                                          highlightthickness=0,
                                          command=lambda: self.start_recording(), relief="flat")
        self.button_record_passive.place(x=218.0, y=42.0, width=34.0, height=34.0)

        # stop
        self.image_stop = PhotoImage(file=relative_to_assets("stop.png"))
        self.button_stop = Button(image=self.image_stop, bg="#1D1D1D", borderwidth=0, highlightthickness=0,
                             command=lambda: self.stop_recording(), relief="flat")
        self.button_stop.place(x=170.0, y=43.0, width=32.0, height=32.0)

        # pause
        self.image_pause = PhotoImage(file=relative_to_assets("pause.png"))
        self.button_pause = Button(image=self.image_pause, bg="#1D1D1D", borderwidth=0, highlightthickness=0,
                              command=lambda: self.pause_tracks(), relief="flat")
        self.button_pause.place(x=115.0, y=43.0, width=23.272737503051758, height=32.0)

        # play
        self.image_play = PhotoImage(file=relative_to_assets("play.png"))
        self.button_play = Button(image=self.image_play, bg="#1D1D1D", borderwidth=0, highlightthickness=0,
                             command=lambda: self.play_tracks(), relief="flat")
        self.button_play.place(x=56.00006103515625, y=41.0, width=42.62738037109375, height=36.57235336303711)

    def redraw(self,window,canvas):
        self.canvas.place(x=0,y=0)
        self.canvas.update()
        """self.top_canvas.config(width=window.winfo_width())
        self.top_canvas.place(x=0, y=self.y)

        self.button_undo.place(x=window.winfo_width() * 0.6, y=(self.y + (96 * 1 / 4)), width=16.0, height=16.0)
        self.button_redo.place(x=window.winfo_width() * 0.6 +16 + 8, y=(self.y + (96 * 1 / 4)), width=16.0, height=16.0)
        self.button_ear.place(x=window.winfo_width() * 0.6, y=(self.y + (96 * 3 / 4) - 16), width=16.0, height=16.0)"""

    def start_recording(self):
        self.context.RECORDING = True
        self.button_recordactive.tkraise()

        self.play_tracks()

    def stop_recording(self):
        self.context.RECORDING = False
        self.button_record_passive.tkraise()

    def expand_speaker(self):
        pass

    def expand_mics(self):
        pass

    def play_track(self, track):
        """ Tries out edited version first, then raw """
        print("[TOPBAR] Playing Track" + str(track.ID))

        try:
            filename = "recordings/edited/track" + str(track.ID) + ".wav"
            data, fs = sf.read(filename, dtype='float32')
            sd.play(data, fs)
        except:
            filename = "recordings/raw/track" + str(track.ID) + ".wav"
            data, fs = sf.read(filename, dtype='float32')
            sd.play(data, fs)

    def play_tracks(self):
        """ Plays every non muted track via thread """
        try:
            for track in self.context.TRACKS:       # play every non muted track simultaneously
                if track.MUTE == False:
                    threading.Thread(target=self.play_track, args=(track,), ).start()

        except Exception as e:
            print("[ERROR] Playing tracks. No recording?")
            print(e)

    def pause_tracks(self):
        sd.stop()

    def import_file(self):
        """ Imports .wav files selected by user """
        # select file
        filename = fd.askopenfilename()
        self.context.DELETE_WORK_FRAME = True
        self.context.IMPORTED_TRACK = filename



    def export(self):

        print("[TOPBAR] Exporting Audio ...")
        exported = AudioSegment.empty()

        first_track = True
        for track in self.context.TRACKS:
            if first_track:
                exported = AudioSegment.from_file("recordings/edited/track" + str(track.ID) + ".wav")
                first_track = False
            else:
                # try edited
                try:
                    track_edited = AudioSegment.from_file("recordings/edited/track" + str(track.ID) + ".wav")
                    exported = exported.overlay(track_edited)
                # pick raw
                except:
                    track_raw = AudioSegment.from_file("recordings/raw/track" + str(track.ID) + ".wav")
                    exported = exported.overlay(track_raw)

        # save combined
        exported.export("recordings/exported/export.wav", format="wav")
        print("[TOPBAR] Exporting Done!")

    def preview(self):

        print("[TOPBAR] Previewing Audio ...")
        exported = AudioSegment.empty()

        first_track = True
        for track in self.context.TRACKS:
            if first_track:
                exported = AudioSegment.from_file("recordings/edited/track" + str(track.ID) + ".wav")
                first_track = False
            else:
                # try edited
                try:
                    track_edited = AudioSegment.from_file("recordings/edited/track" + str(track.ID) + ".wav")
                    exported = exported.overlay(track_edited)
                # pick raw
                except:
                    track_raw = AudioSegment.from_file("recordings/raw/track" + str(track.ID) + ".wav")
                    exported = exported.overlay(track_raw)

        # save combined
        play(exported)
        print("[TOPBAR] Preview Done!")

    def toggle_direct_monitoring(self):
        self.context.DIRECT_MONITORING = not self.context.DIRECT_MONITORING

        # update ui
        if self.context.DIRECT_MONITORING:
            self.image_ear = PhotoImage(file=relative_to_assets("ear_active.png"))
            self.button_ear = Button(image=self.image_ear, borderwidth=0, bg="#1D1D1D", highlightthickness=0,
                                     command=lambda: self.toggle_direct_monitoring(), relief="flat")
            self.button_ear.place(x=842.0, y=36.0, width=18.0, height=18.0)
        else:
            self.image_ear = PhotoImage(file=relative_to_assets("ear.png"))
            self.button_ear = Button(image=self.image_ear, borderwidth=0, bg="#1D1D1D", highlightthickness=0,
                                     command=lambda: self.toggle_direct_monitoring(), relief="flat")
            self.button_ear.place(x=842.0, y=36.0, width=18.0, height=18.0)