import numpy as np
import random
import time
import pandas

from keras.callbacks import LambdaCallback

from keras import optimizers
from keras.layers import Activation, Input, LSTM, Dense, Dropout, BatchNormalization, GRU, Flatten, TimeDistributed
from keras.models import Model
from keras.utils import plot_model
from keras.layers.merge import concatenate

from pandas import read_csv
from socketIO_client import SocketIO, LoggingNamespace
from Audio.Components.MidiPlayer import MidiPlayer

# from keras.utils.vis_utils import model_to_dot
# from matplotlib import pyplot
# from IPython.display import SVG
# import pydot
# import graphviz

from Audio.Components.helpers.prepare_arrays import prepare_notes, prepare_lengths
from Audio.Components.helpers.save_model import save_model
from Audio.Components.helpers.predict import make_prediction
from Audio.Components.helpers.create_categorical_indicies import create_category_indicies
from Audio.Components.helpers.generate_phrases import generate_phrases
from Audio.Components.helpers.decode_predictions import decode_predictions
from Audio.Components.helpers.play_generated_phrase import play_generated_phrase
import constants

# Initialized the players
# socket = SocketIO('localhost', 9876, LoggingNamespace)
player = MidiPlayer()

dropout = 0.2
n_time_steps = constants.n_time_steps
semi_redundancy_step = 3

corpus = read_csv('Audio/data/output.csv', header=1)
print('corpus length:', len(corpus))

notes_corpus = corpus.values[:, 0]
length_corpus = corpus.values[:, 1]

categorized_variables = {
    'note_categories': prepare_notes(),
    'length_categories': prepare_lengths()
}

note_index, index_note = create_category_indicies(categorized_variables['note_categories'])
lengths_index, index_lengths = create_category_indicies(categorized_variables['length_categories'])

lookup_indicies = {
    'note_index': note_index,
    'index_note': index_note,
    'lengths_index': lengths_index,
    'index_lengths': index_lengths,
}

note_phrases, next_note = generate_phrases(notes_corpus, n_time_steps, semi_redundancy_step)
length_phrases, next_length = generate_phrases(length_corpus, n_time_steps, semi_redundancy_step)

# def vectorize_phrases(category):
#
#     return vectorized_x, vectorized_y

note_x = np.zeros((len(note_phrases), n_time_steps, len(categorized_variables['note_categories'])), dtype=np.bool)
note_y = np.zeros((len(note_phrases), len(categorized_variables['note_categories'])), dtype=np.bool)

length_x = np.zeros((len(length_phrases), n_time_steps, len(categorized_variables['length_categories'])), dtype=np.bool)
length_y = np.zeros((len(length_phrases), len(categorized_variables['length_categories'])), dtype=np.bool)

for i, phrase in enumerate(note_phrases):
    for t, note in enumerate(phrase):
        print(i, t, note)
        note_x[i, t, note_index[note]] = 1
    note_y[i, note_index[next_note[i]]] = 1

for i, phrase in enumerate(length_phrases):
    for t, length in enumerate(phrase):
        print(i, t, length)
        length_x[i, t, lengths_index[length]] = 1
    length_y[i, lengths_index[next_length[i]]] = 1


print(note_x.shape)
print(length_x.shape)
print(note_y.shape)
print(length_y.shape)


lstm_size = 64

note_input = Input(name='note_input', shape=(n_time_steps, len(categorized_variables['note_categories'])))
length_input = Input(name='length_input', shape=(n_time_steps, len(categorized_variables['length_categories'])))

note_branch = LSTM(lstm_size, return_sequences=True)(note_input)
note_share = LSTM(int(lstm_size/4), return_sequences=True)(note_branch)

length_branch = LSTM(lstm_size, return_sequences=True)(length_input)
length_share = LSTM(int(lstm_size/4), return_sequences=True)(length_branch)

length_merge = concatenate([length_branch, note_share])
note_merge = concatenate([note_branch, length_share])

length_lstm = LSTM(lstm_size, return_sequences=False)(length_merge)
note_lstm = LSTM(lstm_size, return_sequences=False)(note_merge)

output_notes = Dense(len(categorized_variables['note_categories']), activation='softmax', name='note_output')(note_lstm)
length_output = Dense(len(categorized_variables['length_categories']), activation='softmax', name='length_output')(length_lstm)

optimizer = optimizers.RMSprop(lr=0.001)
model = Model(inputs=[note_input, length_input], outputs=[output_notes, length_output])
model.compile(loss=['categorical_crossentropy', 'categorical_crossentropy'], optimizer=optimizer)


# model.summary()
# SVG(model_to_dot(model).create(prog='dot', format='svg'))

def on_epoch_end(epoch, logs):
    # Function invoked at end of each epoch. Prints generated text.
    if epoch % 1 == 0 and epoch > 3:
        print('----- Generating melody after Epoch: %d' % epoch)

        start_index = 0
        for diversity in [1]:
            print('----- diversity:', diversity)

            generated_notes = []
            generated_lengths = []
            current_note_phrase = notes_corpus[start_index: start_index + n_time_steps]
            current_length_phrase = length_corpus[start_index: start_index + n_time_steps]
            generated_notes.extend(current_note_phrase)
            generated_lengths.extend(current_length_phrase)

            n_to_generate = 20
            start_time = time.time()

            phrases = {'note_phrase': current_note_phrase, 'length_phrase': current_length_phrase}

            for step in range(n_to_generate):
                encoded_prediction = make_prediction(
                    model=model,
                    phrases=phrases,
                    categorized_variables=categorized_variables,
                    lookup_indicies=lookup_indicies,
                    n_time_steps=n_time_steps
                )

                predictions = decode_predictions(
                    encoded_prediction=encoded_prediction,
                    lookup_indicies=lookup_indicies,
                    diversity=diversity
                )

                generated_notes.append(predictions['note_prediction'])
                generated_lengths.append(predictions['length_prediction'])

                phrases['note_phrase'] = np.append(phrases['note_phrase'][1:], predictions['note_prediction'])
                phrases['length_phrase'] = np.append(phrases['length_phrase'][1:], predictions['length_prediction'])

            end_time = time.time()

            play_generated_phrase(
                generated_notes=generated_notes,
                generated_lengths=generated_lengths,
                player=player)

play_callback = LambdaCallback(on_epoch_end=on_epoch_end)

model.fit([note_x, length_x], [note_y, length_y],
          batch_size=256,
          epochs=10,
          callbacks=[play_callback]
          )

save_model(model, 'model')
