""" CONTAINS STATIC VARIABLES """

class Context:

    def __init__(self):

        # STATES
        self.RECORDING = False
        self.DIRECT_MONITORING = False
        self.TRACKS = []

        # AUDIO SETTINGS
        self.sampling = 44100
        self.bitdepth = 16

        # UI UPDATE STATES
        self.IMPORT_DONE = False    # trigger after imported song, to remove work_frame and add track
        self.UPDATEUI_SOLO = False  # trigger for refreshing solo states of tracks
        self.DELETE_HINTS = False   # trigger to remove startup hints

        self.IMPORTED_TRACK = ""

        # UI
        self.current_window = "none"