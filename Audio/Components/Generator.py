import numpy as np
import pyaudio
import time
from Audio.Components.MidiPlayer import MidiPlayer
from Audio.Components.StreamToFrequency import StreamToFrequency
from Audio.Components.Store import Store
from Audio.Components.File_Writer import File_Writer
from Audio.Components.WebSocketPlayer import WebSocketPlayer

from Audio.Components.helpers.logger import logger
from Audio.Components.helpers.load_model import load_model
from Audio.Components.helpers.midi_to_hertz import midi_to_hertz
from Audio.Components.helpers.prepare_arrays import prepare_notes, prepare_lengths
from Audio.Components.helpers.create_categorical_indicies import create_category_indicies
from Audio.Components.helpers.predict import make_prediction
from Audio.Components.helpers.decode_predictions import decode_predictions
from Audio.Components.helpers.sample import sample

from Audio.Player.osc import SineOsc


class Generator:
    def __init__(self, args=None):
        self.arguments = args
        self.write_csv = args.write_csv
        self.play_midi = args.play_midi
        self.show_prediction = args.display_prediction
        self.play_websocket = args.play_websocket
        self.display_volume = args.display_volume
        self.filtered = args.filtered
        self.nn = args.nn
        self.wave = args.wave

        self.writer = File_Writer(write=self.write_csv)
        self.store = Store()
        self.detector = StreamToFrequency(store=self.store, show_volume=self.display_volume)

        """Players"""
        self.osc = SineOsc()
        self.player = self.setup_midi_player()
        self.websocket_player = self.setup_websocket_player()

        """Trained_Model"""
        if args.nn:
            self.n_time_steps = 12
            self.notes = prepare_notes()
            self.lengths = prepare_lengths()

            self.note_index, self.index_note = create_category_indicies(category=self.notes)

            self.length_index, self.index_length = create_category_indicies(category=self.lengths)
            self.model = load_model()

        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paFloat32,
                                  channels=1,
                                  rate=44100,
                                  frames_per_buffer=2048,
                                  input=True,
                                  output=False,
                                  stream_callback=self.detector.callback)

    def setup_websocket_player(self):
        wsp = WebSocketPlayer()
        if self.play_websocket:
            wsp.connect_to_socket()
        return wsp

    def setup_midi_player(self):
        player = None
        if self.play_midi or self.nn:
            try:
                player = MidiPlayer()
                logger('Connected')
            except:
                print('No midi destinations!')
        return player

    def generate(self):
        while True:
            self.play()
            time.sleep(0.0001)

    def beyond_threshold(self):
        threshold = True
        if self.filtered:
            threshold = self.store.new_note
        return threshold

    def make_prediction(self):
        # phrases = {'note_phrase': self.store.note_ring_buffer, 'length_phrase': self.store.length_ring_buffer}
        # categorized_variables = {
        #     'note_categories': self.notes,
        #     'length_categories': self.lengths
        # }
        # lookup_indicies = {
        #     'note_index': self.note_index,
        #     'index_note': self.index_note,
        #     'lengths_index': self.length_index,
        #     'index_lengths': self.index_length,
        # }
        # encoded_prediction = make_prediction(
        #     model=self.model,
        #     phrases=phrases,
        #     categorized_variables=categorized_variables,
        #     lookup_indicies=lookup_indicies,
        #     n_time_steps=self.n_time_steps
        # )
        #
        # predictions = decode_predictions(
        #     encoded_prediction=encoded_prediction,
        #     lookup_indicies=lookup_indicies,
        #     diversity=1
        # )
        note_pred = np.zeros((1, self.n_time_steps, len(self.notes)))
        length_pred = np.zeros((1, self.n_time_steps, len(self.lengths)))
        #
        for t, event in enumerate(self.store.note_ring_buffer):
            note_pred[0, t, self.note_index[event]] = 1.

        for t, event in enumerate(self.store.length_ring_buffer):
            length_pred[0, t, self.length_index[event]] = 1.

        prediction = self.model.predict([note_pred, length_pred], verbose=0)

        note_pred = prediction[0][0]
        length_pred = prediction[1][0]

        note_index_from_sample = sample(note_pred, 1.0)
        note_prediction = self.index_note[note_index_from_sample]

        length_index_from_sample = sample(length_pred, 1.0)
        length_prediction = self.index_length[length_index_from_sample]

        return note_prediction, length_prediction

    def play(self):
        note = self.store.note
        volume = self.store.volume
        length = self.store.length

        if self.beyond_threshold():
            if self.store.past_prediction['length'] > 0:
                if self.write_csv:
                    self.writer.write_to_csv(self.store.past_prediction)

                if self.play_midi:
                    self.player.play(note, self.store.length, volume)

                if self.play_websocket:
                    self.websocket_player.play(note)

                if self.show_prediction:
                    print(self.store.past_prediction)

                if self.wave:
                    hertz = midi_to_hertz(note)
                    self.osc.freq = hertz
                    # self.osc.freq = note

                if self.nn:
                    predicted_note, predicted_length = self.make_prediction()
                    print(predicted_note, predicted_length)
                    velocity = 100
                    if predicted_note > 70:
                        predicted_note = 0
                    self.player.play(predicted_note, predicted_length, velocity)

        self.store.past_prediction = self.store.values
