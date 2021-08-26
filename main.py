import pyaudio
import wave
import PySimpleGUI as sg
import threading
import sounddevice as sd
import soundfile as sf

def refresh_window(recording):
    global window

    function_col = [
        [sg.Button('Play', button_color=("#1D1D1D", "#1D1D1D"), image_filename=r'./ButtonGraphics/play.png',
                   image_subsample=3, border_width=0),
         sg.Button('Pause', button_color=("#1D1D1D", "#1D1D1D"), image_filename=r'./ButtonGraphics/pause.png',
                       image_subsample=3, border_width=0),
        sg.Button('Stop', button_color=("#1D1D1D", "#1D1D1D"), image_filename=r'./ButtonGraphics/stop.png',
                       image_subsample=3, border_width=0)
         ]]
    if recording:
        function_col[0].append(sg.Button('Record', button_color=("#1D1D1D", "#1D1D1D"), image_filename=r'./ButtonGraphics/record.png',
                       image_subsample=3, border_width=0))

    else:
            function_col[0].append(sg.Button('Record', button_color=("#1D1D1D", "#1D1D1D"), image_filename=r'./ButtonGraphics/record_passive.png',
                       image_subsample=3, border_width=0))

    function_col[0].append(sg.Button('transparent0', button_color=("#1D1D1D", "#1D1D1D"),
                       image_filename=r'./ButtonGraphics/transparent.png', image_subsample=2, border_width=0))
    function_col[0].append(sg.Button('transparent1', button_color=("#1D1D1D", "#1D1D1D"),
                       image_filename=r'./ButtonGraphics/transparent.png', image_subsample=2, border_width=0))
    function_col[0].append(sg.Button('transparent2', button_color=("#1D1D1D", "#1D1D1D"),
                       image_filename=r'./ButtonGraphics/transparent.png', image_subsample=2, border_width=0))
    function_col[0].append(sg.Button('DIRECT MONITORING', button_color=("#1D1D1D", "#1D1D1D"),
                       image_filename=r'./ButtonGraphics/direct_monitoring.png', image_subsample=3, border_width=0))
    function_col[0].append(sg.Button('PLAY RECORDED WHILE RECORD', button_color=("#1D1D1D", "#1D1D1D"),
                       image_filename=r'./ButtonGraphics/play_recorded.png', image_subsample=3, border_width=0))

    frame_layout = [
        [sg.Column(function_col, background_color="#1D1D1D")],
    ]

    layout = [

        [
            sg.Frame('', frame_layout, font='Any 12', title_color='#1D1D1D', border_width=0, background_color="#1D1D1D")
        ],

        [
            sg.Text("Audio Options", background_color="#292929", border_width=0),
            sg.Button("Bitrate", button_color=("white", "#292929"), border_width=0),
            sg.Button("Samplerate", button_color=("white", "#292929"), border_width=0),
            sg.Button("Stereo/Mono", button_color=("white", "#292929"), border_width=0),
        ],

    ]

    window1 = sg.Window('AuPaCity RECORDING',layout, margins = (0,35), background_color='#111111')
    window.Close()
    window = window1

audio = pyaudio.PyAudio()

# STATES
RECORDING  = False
DIRECT_MONITORING = False
PLAY_WHILE_RECORD = False

# AUDIO OPTIONS
BIT_RATE = pyaudio.paInt16
SAMPLING_RATE = 44100
CHUNK_SIZE = 1024
CHANNELS = 1


# Audio Setup
stream_in = audio.open(format=BIT_RATE, channels=CHANNELS, rate=SAMPLING_RATE, input=True, frames_per_buffer=CHUNK_SIZE)
stream_out1 = audio.open(format=BIT_RATE, channels=CHANNELS, rate=SAMPLING_RATE, output=True, frames_per_buffer=CHUNK_SIZE)
stream_out2 = audio.open(format=BIT_RATE, channels=CHANNELS, rate=SAMPLING_RATE, output=True, frames_per_buffer=CHUNK_SIZE)
frames = []
spuren = []
spurnummer = 0

# UI Setup
function_col = [
            [   sg.Button('Play',  button_color=("#1D1D1D", "#1D1D1D"), image_filename=r'./ButtonGraphics/play.png',  image_subsample=3, border_width=0),
                sg.Button('Pause', button_color=("#1D1D1D", "#1D1D1D"), image_filename=r'./ButtonGraphics/pause.png', image_subsample=3, border_width=0),
                sg.Button('Stop',  button_color=("#1D1D1D", "#1D1D1D"), image_filename=r'./ButtonGraphics/stop.png',  image_subsample=3, border_width=0),
                sg.Button('Record',button_color=("#1D1D1D", "#1D1D1D"), image_filename=r'./ButtonGraphics/record_passive.png',image_subsample=3, border_width=0),
                sg.Button('transparent0', button_color=("#1D1D1D", "#1D1D1D"),image_filename=r'./ButtonGraphics/transparent.png', image_subsample=2, border_width=0),
                sg.Button('transparent1', button_color=("#1D1D1D", "#1D1D1D"),image_filename=r'./ButtonGraphics/transparent.png', image_subsample=2, border_width=0),
                sg.Button('transparent2', button_color=("#1D1D1D", "#1D1D1D"),image_filename=r'./ButtonGraphics/transparent.png', image_subsample=2, border_width=0),
                sg.Button('DIRECT MONITORING', button_color=("#1D1D1D", "#1D1D1D"),image_filename=r'./ButtonGraphics/direct_monitoring.png', image_subsample=3, border_width=0),
                sg.Button('PLAY RECORDED WHILE RECORD', button_color=("#1D1D1D", "#1D1D1D"),image_filename=r'./ButtonGraphics/play_recorded.png', image_subsample=3, border_width=0),
            ]
]


frame_layout = [
                    [sg.Column(function_col,background_color="#1D1D1D")],
]

layout = [

            [
                sg.Frame('', frame_layout, font='Any 12', title_color='#1D1D1D', border_width=0, background_color="#1D1D1D",)
            ],

            [
                sg.Text("Audio Options",background_color="#292929",border_width=0),
                sg.Button("Bitrate",button_color=("white", "#292929"),border_width=0),
                sg.Button("Samplerate",button_color=("white", "#292929"),border_width=0),
                sg.Button("Stereo/Mono",button_color=("white", "#292929"),border_width=0),
            ],

]

# Look
window = sg.Window("AuPaCity", layout, margins = (0,35), background_color='#111111')


def start_recording():
    """ Error occurs when recording third spur """
    global  stream_in
    global stream_out1
    global stream_out2
    global spurnummer
    global DIRECT_MONITORING
    global PLAY_WHILE_RECORD

    # AUDIO IN AUDIO OUT
    frames = []
    frame = 0
    stream_in = audio.open(format=BIT_RATE, channels=CHANNELS, rate=SAMPLING_RATE, input=True,
                           frames_per_buffer=CHUNK_SIZE)
    if DIRECT_MONITORING or PLAY_WHILE_RECORD:
        stream_out1 = audio.open(format=BIT_RATE, channels=CHANNELS, rate=SAMPLING_RATE, output=True,
                                frames_per_buffer=CHUNK_SIZE)
        stream_out2 = audio.open(format=BIT_RATE, channels=CHANNELS, rate=SAMPLING_RATE, output=True,
                                 frames_per_buffer=CHUNK_SIZE)

    # NEUE SPUR AUFNEHMEN
    while RECORDING:
        try:

            # MIKROFON INHALT
            data = stream_in.read(CHUNK_SIZE, exception_on_overflow=False)
            frames.append(data)

            # DIREKTE WIEDERGABE ?
            if DIRECT_MONITORING:
                stream_out1.write(data)

            # VORHERIGE SPUR WIEDERGEBEN?
            if len(spuren) > 0 and PLAY_WHILE_RECORD:
                try:
                    stream_out2.write(bytes(spuren[0][frame]))
                    frame += 1
                except:
                    print("Vorherige Spur fertig gespielt")
                    PLAY_WHILE_RECORD = False

        except Exception as e:
            print(e)
            return

    # SPUR SPEICHERN ALS WAV
    spurnummer = str(len(spuren))
    stream_in.stop_stream()
    stream_in.close()
    stream_out1.stop_stream()
    stream_out2.stop_stream()
    stream_out1.close()
    stream_out2.close()
    audio.terminate()
    sound_file = wave.open("spur" + str(spurnummer) + ".wav", "wb")
    sound_file.setnchannels(CHANNELS)
    sound_file.setsampwidth(audio.get_sample_size(BIT_RATE))
    sound_file.setframerate(SAMPLING_RATE)
    sound_file.writeframes(b''.join(frames))
    sound_file.close()
    spuren.append(frames)
    print("Spur gespeichert unter: " + "spur" + str(spurnummer) + ".wav")

# UI LOOP
while True:
    plot = 0
    event, values = window.read()

    if event == "Bitrate":
        if not RECORDING:
            if BIT_RATE == pyaudio.paInt32:
                BIT_RATE = pyaudio.paInt16
                print("Bitrate changed to 16")
            else:
                BIT_RATE = pyaudio.paInt32
                print("Bitrate changed to 32")

    if event == "Samplerate":
        if not RECORDING:
            if SAMPLING_RATE == 44100:
                SAMPLING_RATE = 48000
            elif SAMPLING_RATE == 48000:
                SAMPLING_RATE = 96000
            elif SAMPLING_RATE == 96000:
                SAMPLING_RATE = 44100
            print("Sampelrate changed to " + str(SAMPLING_RATE))

    if event == "Stereo/Mono":
        if not RECORDING:
            if CHANNELS == 1:
                CHANNELS = 2
            else:
                CHANNELS = 1
            print("Channels changed to " + str(CHANNELS))

    if event == "DIRECT MONITORING":
        if not RECORDING:
            DIRECT_MONITORING = not DIRECT_MONITORING
            print("Direct Monetoring " + str(DIRECT_MONITORING))

    if event == "PLAY RECORDED WHILE RECORD":
        if not RECORDING:
            if not PLAY_WHILE_RECORD:
                print("Spuren werden wiedergegeben beim aufnehmen")
                PLAY_WHILE_RECORD = not PLAY_WHILE_RECORD
            else:
                print("Spuren werden nicht wiedergegeben beim aufnehmen")
                PLAY_WHILE_RECORD = not PLAY_WHILE_RECORD

    # RECORD
    if event == "Record":
        refresh_window(True)
        if not RECORDING:
            try:
                RECORDING = not RECORDING
                print("Recording STARTED")
                threading.Thread(target=start_recording).start()
            except:
                print("Recording ERROR?!")

    # STOP RECORD
    if event == "Stop":
        refresh_window(False)
        if RECORDING:
            print("Recording STOPPED")
            RECORDING = not RECORDING

    # PLAY RECORD
    if event == "Play":
        """ TODO: Spielt Spur 0 ab aber bei 1 gibt es Fehler. """
        if not RECORDING:
            print("Spiele spur" + str(spurnummer) + ".wav")
            filename = "spur" + str(spurnummer) + ".wav"
            data, fs = sf.read(filename, dtype='float32')
            sd.play(data, fs)
            status = sd.wait()  # Wait until file is done playing

    # CLOSE PROGRAM
    if event == sg.WIN_CLOSED:
        RECORDING = False
        break


window.close()