from math import pi
import math
import numpy as np
import random

class SineOsc:
    def __init__(self):
        self.rate = 44100
        self.freq = 20

    def wave(self, frequency):
        """produces sine across np array"""

        length = math.floor(self.rate/frequency)
        diff = self.rate - length * frequency
        error = diff/length
        print(frequency, error)
        factor = float(frequency + error) * (pi * 2) / self.rate
        waveform = np.sin(np.arange(length) * factor)
        # print(length, frequency, factor)

        return waveform

    def start_osc(self, stream):
        count = 0
        while self.freq < 1200:
            wave = self.wave(self.freq)
            stream.write(wave.astype(np.float32).tostring())

            if count % 1 == 0:
                self.freq += 1
            # print(count)
            count += 1


            # self.waveform[300] = np.multiply(waveform[:attack], fade_in)


        # count = 0
        # for i in wave1:
        #     if -.001 < i < .001:
        #         count += 1
        #         print(count, i)





        # while True:
        #     wave = self.wave(self.freq, length, self.sample_rate)
