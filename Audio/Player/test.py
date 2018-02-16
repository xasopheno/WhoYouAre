import random
import pyaudio
import os
import sys
import multiprocessing as mp
import time
from osc import SineOsc

osc = SineOsc()

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=44100,
                output=1,
                )


def test():
    osc.start_osc(stream)


def func1():
    print ('func2')
    volume = 2
    length = .7
    freq = 300
    while True:
        osc.play_frequencies(stream, length, volume, 1, 1,
                                      freq,
                                  )
        freq = random.randint(300, 400)
        # time.sleep(.1)


if __name__ == '__main__':
    test()
