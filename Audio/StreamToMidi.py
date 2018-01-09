import os.path
import argparse

import pyaudio
import math

import sys
import time
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
current_path = os.getcwd()
from Midi.MidiPlayer import MidiPlayer
from StreamToFrequency import StreamToFrequency
from Store import Store

class Generator:
    def __init__(self, args=None, store=None):
        self.arguments = args
        self.subdivision = 0.1
        self.isZero = True
        self.counter = 1
        self.past_pred = 0
        self.show_prediction = args.display_prediction

        self.volume_array = []

        self.detector = StreamToFrequency(store=store, show_volume=args.display_volume)
        self.store = store
        self.player = MidiPlayer(synth='Volca')

        self.p = pyaudio.   PyAudio()
        self.stream = self.p.open(format=pyaudio.paFloat32,
                                  channels=1,
                                  rate=44100,
                                  frames_per_buffer=2048,
                                  input=True,
                                  output=False,
                                  stream_callback=self.detector.callback)

    def get_store_values(self):
        while True:
            pred = self.store.values

            if self.store.note == self.past_pred:
                self.store.inc_length()
            else:
                self.store.reset()

            self.past_pred = self.store.note

            self.play_value(pred)

    def play_midi(self, value, volume):
        if value == 0:
            time.sleep(self.subdivision * 1.0)
        else:
            for i in range(2):
                self.player.play(value, self.subdivision /3, volume)

    def play_value(self, predicted_values):
        note = predicted_values["note"]
        volume = predicted_values["volume"]

        if self.show_prediction:
            print(predicted_values)

        self.play_midi(note, volume)


def get_user_options():
    a = argparse.ArgumentParser()
    a.add_argument("--volume",
                   help = "Specify if input volume should be displayed.",
                   dest = "display_volume",
                   required=False,
                   default=False,
                   type=bool,
                   nargs=1)

    a.add_argument("--values",
                   help="Specify if prediction values should be displayed).",
                   dest = "display_prediction",
                   required=False,
                   default=False,
                   type=bool,
                   nargs=1)

    return a.parse_args()

if __name__ == '__main__':
    args = get_user_options()
    print('args: ', args)

    store = Store()
    generator = Generator(args=args, store=store)

    generator.get_store_values()
