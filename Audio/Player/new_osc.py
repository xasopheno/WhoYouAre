import threading
import math
import numpy as np
import time
import random
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
        self.chunk_size = 400
        self.freq = 0.0
        self.phase = 0.0
        self.last_freq = 0

        self.fade_in = np.arange(0., 1., 1./self.chunk_size)
        self.fade_out = np.arange(1., 0., -1./self.chunk_size)

        thread = threading.Thread(target=self.oscillator)
        thread.daemon = True
        thread.start()

    def update_phase(self, freq):
        self.phase += freq * self.chunk_size * self.tau / self.rate
        self.phase %= self.tau

    def make_chunk(self, freq):
        if freq == 0:
            chunk = np.zeros(self.chunk_size)
            return chunk
        phase = (np.arange(self.chunk_size) * (freq * self.tau / self.rate)) + self.phase
        phase %= self.tau
        chunk = np.sin(phase) / 10
        return chunk

    def portamento(self):
        diff = self.last_freq - self.freq
        if diff > 0:
            while self.last_freq > self.freq:
                chunk = self.make_chunk(self.last_freq)
                self.write_to_stream(chunk, self.last_freq)
                self.last_freq -= 40
        else:
            while self.last_freq < self.freq:
                chunk = self.make_chunk(self.last_freq)
                self.write_to_stream(chunk, self.last_freq)
                self.last_freq += 40

    def write_attack(self):
        chunk = self.make_chunk(self.freq)
        chunk[:self.chunk_size] = np.multiply(chunk[:self.chunk_size], self.fade_in)
        self.write_to_stream(chunk, self.freq)

    def write_decay(self):
        chunk = self.make_chunk(self.last_freq)
        chunk[-self.chunk_size:] = np.multiply(chunk[-self.chunk_size:], self.fade_out)
        self.write_to_stream(chunk, 0)

    def manage_transition(self):
        if self.last_freq != self.freq:
            if self.freq == 0:
                self.write_decay()
            elif self.last_freq == 0:
                self.write_attack()
            else:
                self.portamento()
        self.last_freq = self.freq

    def write_to_stream(self, chunk, freq):
        self.update_phase(freq)
        self.stream.write(chunk.astype(np.float32).tostring())

    def run(self):
        self.manage_transition()
        chunk = self.make_chunk(self.freq)
        self.write_to_stream(chunk, self.freq)

    def oscillator(self):
        while True:
            self.run()

osc = SineOsc()

if __name__ == "__main__":
    print('Oscillator test...')
    while True:
        rand = random.randint(0, 2)
        if rand == 0:
            osc.freq = 0
        else:
            osc.freq = random.randint(100, 400)
        time.sleep(.5)
