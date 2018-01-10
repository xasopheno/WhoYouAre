import os.path
import argparse
import pyaudio
import sys
import time
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
from Audio.MidiPlayer import MidiPlayer
from Audio.StreamToFrequency import StreamToFrequency
from Audio.Store import Store
from Audio.File_Writer import File_Writer


class Generator:
    def __init__(self, args=None):
        self.arguments = args
        self.subdivision = 0.1
        self.isZero = True
        self.counter = 1
        self.past_pred = 0
        self.show_prediction = args.display_prediction
        self.new_note = False
        self.write_csv = args.write_csv
        self.writer = File_Writer()

        self.volume_array = []

        self.store = Store()
        self.detector = StreamToFrequency(store=self.store, show_volume=args.display_volume)

        self.play = args.play
        self.player = self.setup_player()

        self.p = pyaudio.   PyAudio()
        self.stream = self.p.open(format=pyaudio.paFloat32,
                                  channels=1,
                                  rate=44100,
                                  frames_per_buffer=2048,
                                  input=True,
                                  output=False,
                                  stream_callback=self.detector.callback)

    def setup_player(self):
        player = None
        if self.play:
            try:
                player = MidiPlayer(synth='Volca')
            except:
                print('No midi desinations!')
        return player

    def generate(self):
        while True:
            pred = self.store.values

            if self.store.note == self.past_pred:
                self.store.inc_length()
                self.new_note = False
            else:
                self.new_note = True
                self.store.reset()

            self.past_pred = self.store.note

            self.play_value(pred)

    def play_value(self, predicted_values):
        note = predicted_values["note"]
        volume = predicted_values["volume"]

        if self.show_prediction and self.new_note:
            print(predicted_values)

        if self.write_csv and self.new_note:
            self.writer.write_to_csv(predicted_values)

        self.play_midi(note, volume)

    def play_midi(self, value, volume):
        if value == 0:
            time.sleep(self.subdivision * 1.0)
        else:
            for i in range(2):
                if self.play:
                    self.player.play(value, self.subdivision / 3, volume)
                else:
                    time.sleep(self.subdivision / 3)
