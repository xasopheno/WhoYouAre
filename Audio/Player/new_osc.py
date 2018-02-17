import threading
import math
import numpy as np
import time
import pyaudio


class SineOsc:
    def __init__(self):
        p = pyaudio.PyAudio()
        self.rate = 44100
        self.stream = p.open(format=pyaudio.paFloat32,
                             channels=1,
                             rate=self.rate,
                             output=1)

        self.tau = math.pi * 2
        self.chunk_size = 100
        self.freq = 300
        self.phase = 0.0

        thread = threading.Thread(target=self.update_freq, args=())
        thread.daemon = True
        thread.start()

    def update_phase(self):
        self.phase += self.freq * self.chunk_size * self.tau / self.rate
        self.phase %= self.tau

    def make_chunk(self):
        phase = (np.arange(self.chunk_size) * (self.freq * self.tau / self.rate)) + self.phase
        phase %= self.tau
        waveform = np.sin(phase)
        return waveform

    def write(self):
        chunk = self.make_chunk()
        self.update_phase()
        self.stream.write(chunk.astype(np.float32).tostring())

    def update_freq(self):
        while True:
            self.write()

osc = SineOsc()

while True:
    osc.freq += 1
    time.sleep(.01)
