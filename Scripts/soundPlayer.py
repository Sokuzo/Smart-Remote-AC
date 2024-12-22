#Import library
from pydub import AudioSegment
from pydub.playback import play
from threading import Lock
import time


enableAudio = True

minInterval = 0.4
last_play_time = time.time()
last_play_time_lock = Lock()

#Bunyikan suara saat suatu tombol ditekan
def soundBeep(min_interval=minInterval):
    global last_play_time

    if enableAudio:
        current_time = time.time()
        if current_time - last_play_time >= min_interval:
            last_play_time = current_time
            sound = AudioSegment.from_file("Audio/beep.wav")
            play(sound)

#Bunyikan suara saat timer habis
def soundTimer(min_interval=minInterval):
    global last_play_time

    if enableAudio:
        current_time = time.time()
        if current_time - last_play_time >= min_interval:
            last_play_time = current_time
            sound = AudioSegment.from_file("Audio/timer.wav")
            play(sound)
