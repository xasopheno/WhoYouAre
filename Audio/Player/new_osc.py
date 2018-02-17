from math import pi
import threading
import math
import numpy as np
import random
import time
import pyaudio


class SineOsc():
    def __init__(self):
        p = pyaudio.PyAudio()
        self.rate = 44100
        self.chunk_size = 5
        self.stream = p.open(format=pyaudio.paFloat32,
                    channels=1,
                    rate=self.rate,
                    output=1,
                    # stream_callback=self.write()
                )

        self.freq = 100
        self.phase = 0.0

        thread = threading.Thread(target=self.update_freq, args=())
        thread.daemon = True
        thread.start()

    def update_phase(self):
        self.phase += self.chunk_size * (pi * 2) / self.rate
        self.phase %= (math.pi * 2)
        print(self.phase)

    def make_chunk(self):
        # """produces sine across np array"""

        factor = float(self.freq) * (pi * 2) / self.rate
        phase = (np.arange(self.chunk_size) * (pi * 2) / self.rate + self.phase) % (math.pi * 2)
        # waveform = np.sin(np.arange(length) * factor)
        return phase

    def write(self):
        chunk = self.make_chunk()
        # print(chunk)
        self.update_phase()
        self.stream.write(chunk.astype(np.float32).tostring())


    def update_freq(self):
        print('update')
        while True:
            self.write()



osc = SineOsc()

freq = 20
while True:
    osc.freq = random.randint(100, 1200)
    osc.freq += 1
