import numpy as np
import pyaudio
import time
import threading
import random
import tensorflow as tf

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
from Audio.Components.helpers.make_encoded_prediction import make_encoded_prediction
from Audio.Components.helpers.decode_predictions import decode_predictions
from Audio.Components.helpers.play_generated_phrase import play_generated_phrase
import constants

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
            self.prediction_lock = threading.Lock()
            self.n_time_steps = constants.n_time_steps
            self.notes = prepare_notes()
            self.lengths = prepare_lengths()

            self.categorized_variables = {
                'note_categories': self.notes,
                'length_categories': self.lengths
            }

            self.note_index, self.index_note = create_category_indicies(category=self.notes)
            self.length_index, self.index_length = create_category_indicies(category=self.lengths)

            self.lookup_indicies = {
                'note_index': self.note_index,
                'index_note': self.index_note,
                'lengths_index': self.length_index,
                'index_lengths': self.index_length,
            }

            self.model = load_model()
            self.graph = tf.get_default_graph()

        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paFloat32,
                                  channels=1,
                                  rate=constants.sample_rate,
                                  frames_per_buffer=constants.chunk_size,
                                  input=True,
                                  output=False,
                                  stream_callback=self.detector.callback)

        thread = threading.Thread(target=self.generate_and_play_prediction)
        thread.daemon = True
        thread.start()

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

    def generate_prediction_phrases(self, model, phrases, categorized_variables, lookup_indicies, n_time_steps, diversity, n_to_generate):
        pass

    def generate_predictions(self, temperature=1):
        n_to_generate = random.choice([3, 4, 5, 6])
        print('n_to_generate', n_to_generate)

        generated_notes = []
        generated_lengths = []
        phrases = {'note_phrase': list(self.store.note_ring_buffer), 'length_phrase': list(self.store.length_ring_buffer)}

        for step in range(n_to_generate):
            encoded_prediction = make_encoded_prediction(
                model=self.model,
                phrases=phrases,
                categorized_variables=self.categorized_variables,
                lookup_indicies=self.lookup_indicies,
                n_time_steps=self.n_time_steps
            )

            predictions = decode_predictions(
                temperature=temperature,
                encoded_prediction=encoded_prediction,
                lookup_indicies=self.lookup_indicies,
            )

            generated_notes.append(predictions['note_prediction'])
            generated_lengths.append(predictions['length_prediction'])

            phrases['note_phrase'] = np.append(phrases['note_phrase'][1:], predictions['note_prediction'])
            phrases['length_phrase'] = np.append(phrases['length_phrase'][1:], predictions['length_prediction'])

        return generated_notes, generated_lengths

    def generate_and_play_prediction(self):
        with self.graph.as_default():
            while True:
                generated_notes, generated_lengths = self.generate_predictions(temperature=0.5)
                play_generated_phrase(
                    generated_notes=generated_notes,
                    generated_lengths=generated_lengths,
                    player=self.player)

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
                    print('_____________________', self.store.note_ring_buffer)
                    # print('_____________________', self.store.length_ring_buffer)

        self.store.past_prediction = self.store.values
