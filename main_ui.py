#!/usr/bin/env python

import time
from pathlib import Path
from tkinter import *

import bottom_bar
import top_bar
import work_frame
from libs.ResizingCanvas import ResizingCanvas
from track import MonoTrack

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")
def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)



class MainUI:


    def __init__(self, context):
        """ Creates window """
        self.context = context
        first_time = True
        self.track_started = False
        every_second_frame = True

        self.window = Tk()
        self.window.geometry("1440x1000")
        self.window.configure(bg="#111111")
        self.window.resizable(False, False)
        self.canvas = Canvas(self.window, bg="#111111", height=1000, width=1440, bd=0, highlightthickness=0,relief="flat")
        self.canvas.place(x=0, y=0)
        self.window.update()
        self.canvas.update()

        while True:

            # DRAW DEFAULT UI
            if first_time:
                self.TOP_BAR = top_bar.TopBarUI(self.window, self.canvas, self.context)
                self.WORK_FRAME = work_frame.WorkFrame(self.window, self.canvas, self.context)
                self.BOTTOM_BAR = bottom_bar.BottomBarUI(self.window, self.canvas, self.context)
                first_time = False

            # UPDATES
            self.BOTTOM_BAR.refresh()

            # IMPORT TRIGGER
            if self.context.IMPORT_DONE:
                self.WORK_FRAME.delete()
                self.context.IMPORT_DONE = False
                track = MonoTrack(self.window, self.canvas, self.context, filename=self.context.IMPORTED_TRACK)
                self.context.TRACKS.append(track)
                track.save()

            # DELETE HINTS TRIGGER
            if self.context.DELETE_HINTS:
                self.WORK_FRAME.delete()
                self.context.DELETE_HINTS = False

            # RECORDING JUST STARTED / STOPPED
            if self.context.RECORDING and not self.track_started:           # this means the recording has just started
                self.add_track()
                self.track_started = True
            if not self.context.RECORDING and self.track_started:   # this means the recording has just stopped
                self.track_started = False


            # SOLO TRIGGER
            if self.context.UPDATEUI_SOLO:     # this means a track has just been solo activated
                for track in self.context.TRACKS:
                    if track.SOLO == False:
                        track.set_mute(True)
                self.context.UPDATEUI_SOLO = False

            # RECORDING STATE: ANIMATION
            if self.context.RECORDING:
                self.running_track.animate_recording()
                time.sleep(0.02)    # slow down animation during recording
            else:
                time.sleep(0.0001)   # increase fps for more responsive ui feel

            try:    # necessary for "clean" closing
                self.canvas.update()
                self.window.update()
            except:
                break


    def add_track(self):
        track = MonoTrack(self.window, self.canvas, self.context)
        self.running_track = track          # to define which track is recording right now
        self.context.TRACKS.append(track)
        track.start_recording()
        self.WORK_FRAME.delete()            # if hints are shown, delete them