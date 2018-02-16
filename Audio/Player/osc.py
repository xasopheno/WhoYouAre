from math import pi
import threading
import math
import numpy as np
import random
import time
import pyaudio


class SineOsc():
    def __init__(self, s):
        self.rate = 176400
        self.freq = 100
        self.last_freq = 0
        self.stream = s

        thread = threading.Thread(target=self.update_freq, args=())
        thread.daemon = True
        thread.start()

    def wave(self, frequency):
        """produces sine across np array"""
        length = math.floor(self.rate/frequency)
        diff = self.rate - length * frequency
        error = diff/length
        frequency += error
        factor = float(frequency) * (pi * 2) / self.rate
        waveform = np.sin(np.arange(length) * factor)

        return waveform

    def write(self, freq):
        wave = self.wave(freq) / (freq/100)
        self.stream.write(wave.astype(np.float32).tostring())

    def slide(self):
        diff = self.freq - self.last_freq
        if diff > 0:
            while self.last_freq < self.freq:
                self.last_freq += 20
                self.write(self.last_freq)
        else:
            while self.last_freq > self.freq:
                self.last_freq -= 20
                self.write(self.last_freq)


    def update_freq(self):
        print('update')
        while True:
            if self.freq != self.last_freq:
                self.slide()
                self.last_freq = self.freq
            self.write(self.freq)

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=176400,
                output=1,
                )
osc = SineOsc(stream)

while True:
    osc.freq = random.randint(50, 1200)
    time.sleep(.5)
