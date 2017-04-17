import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt
import urllib.request
from urllib.request import urlopen

def get_audio_analysis(song_url):
    if(song_url is None):
        return None, None, None, None
    response = urlopen(song_url)
    urllib.request.urlretrieve(song_url, "current.mp3")
    y, sr = librosa.load("./current.mp3")

    tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
    #Tempo = beats/minute


    pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
    #pitch = Frequency
    pitch_ave = np.average(pitches)

    harm = np.sum(librosa.effects.harmonic(y))
    perc = np.sum(librosa.effects.percussive(y))


    return tempo, pitch_ave, harm, perc
