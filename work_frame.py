from pathlib import Path
from tkinter import PhotoImage, Label

# PATH STUFF

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./tkinterdesigner/hints")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class WorkFrame:

    def __init__(self, window, canvas, context):
        self.canvas = canvas
        self.context = context

        # background
        self.x = 0
        self.y = 141
        self.color = "#111111"
        self.canvas.create_rectangle(0.0, self.y, 1440.0, 888, fill=self.color, outline='')

        # load hints
        self.img_recording_hint = PhotoImage(file=relative_to_assets('recording_hint.png'))
        self.recording_hint = Label(canvas, image=self.img_recording_hint,borderwidth =0)
        self.recording_hint.place(x=114,y=134)

        # load hints
        self.img_audio_hint = PhotoImage(file=relative_to_assets('audio_hint.png'))
        self.audio_hint = Label(canvas, image=self.img_audio_hint, borderwidth=0)
        self.audio_hint.place(x=40, y=660)

        # load hints
        self.img_effects_hint = PhotoImage(file=relative_to_assets('effects_hint.png'))
        self.effects_hint = Label(canvas, image=self.img_effects_hint, borderwidth=0)
        self.effects_hint.place(x=495, y=660)

        # load hints
        self.img_settings_hint = PhotoImage(file=relative_to_assets('general_settings.png'))
        self.settings_hint = Label(canvas, image=self.img_settings_hint, borderwidth=0)
        self.settings_hint.place(x=985, y=697)

        # load hints
        self.img_export_hint = PhotoImage(file=relative_to_assets('export_hint.png'))
        self.export_hint = Label(canvas, image=self.img_export_hint, borderwidth=0)
        self.export_hint.place(x=1010, y=141)

        # load hints
        self.img_input_hint = PhotoImage(file=relative_to_assets('input_hint.png'))
        self.input_hint = Label(canvas, image=self.img_input_hint, borderwidth=0)
        self.input_hint.place(x=483, y=137)

        self.canvas.create_text(1440/2 - 40, 1000/2, anchor='nw', text="Pre Alpha 1.0 - Dont get angry if bugs occur.", fill='#3E3E3E', font=('Roboto Light', 14))
        self.canvas.create_text(1440 / 2 - 40, 1000 / 2 + 30, anchor='nw', text="Thank you for testing it out.",fill='#3E3E3E', font=('Roboto Light', 14))
        self.canvas.create_text(1440 / 2 - 40, 1000 / 2 + 60, anchor='nw', text="Visit our website to report bugs:", fill='#3E3E3E', font=('Roboto Light', 14))
        self.canvas.create_text(1440 / 2 - 40, 1000 / 2 + 90, anchor='nw', text="https://www.aupycity.com/bug",fill='#3E3E3E', font=('Roboto Light', 14))

        self.hints = [self.input_hint, self.export_hint, self.settings_hint, self.effects_hint, self.audio_hint, self.recording_hint]

    def delete(self):
        try:
            for hint in self.hints:
                hint.destroy()
        except Exception as e:
            print("[WORK_FRAME] DELETING WENT WRONG! Already deleted?")
            print("[ERROR] ", str(e))