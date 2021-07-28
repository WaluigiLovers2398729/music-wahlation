import matplotlib.mlab as mlab
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from typing import Tuple

def get_spectogram(recorded_audio):
    fig, ax = plt.subplots()

    S, freqs, times, im = ax.specgram(
        recorded_audio,
        NFFT=4096,
        Fs=sampling_rate,
        window=mlab.window_hanning,
        noverlap=4096 // 2,
        mode='magnitude',
        scale="dB"
    )
    return S, freqs, times