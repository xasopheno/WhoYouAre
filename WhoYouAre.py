import numpy as np
import time

from keras.callbacks import LambdaCallback
from keras.utils import plot_model

from pandas import read_csv
from Audio.Components.MidiPlayer import MidiPlayer

# from keras.utils.vis_utils import model_to_dot
# from matplotlib import pyplot
# from IPython.display import SVG
# import pydot
# import graphviz

from NN.models.windowed_model import create_model

from Audio.Components.helpers.prepare_arrays import prepare_notes, prepare_lengths
from Audio.Components.helpers.save_model import save_model
from Audio.Components.helpers.predict import make_prediction
from Audio.Components.helpers.create_categorical_indicies import create_category_indicies
from Audio.Components.helpers.generate_phrases import generate_phrases
from Audio.Components.helpers.decode_predictions import decode_predictions
from Audio.Components.helpers.play_generated_phrase import play_generated_phrase
from Audio.Components.helpers.vectorize_phrases import vectorize_phrases
from Audio.Components.helpers.logger import logger
import constants

player = MidiPlayer()

dropout = constants.dropout
n_time_steps = constants.n_time_steps
semi_redundancy_step = constants.semi_redundancy_step
lstm_size = constants.lstm_size
lr = constants.lr
epochs = constants.epochs
batch_size = constants.batch_size
n_to_generate = constants.n_to_generate

corpus = read_csv('Audio/data/output.csv', header=1)
print('corpus length:', len(corpus))

logger('PREPROCESSING')
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

note_x, note_y = vectorize_phrases(
    phrases=note_phrases,
    n_categories=len(categorized_variables['note_categories']),
    n_time_steps=n_time_steps,
    lookup_index=lookup_indicies['note_index'],
    next_lookup_index=next_note
    )

length_x, length_y = vectorize_phrases(
    phrases=length_phrases,
    n_categories=len(categorized_variables['length_categories']),
    n_time_steps=n_time_steps,
    lookup_index=lookup_indicies['lengths_index'],
    next_lookup_index=next_length
)

print(note_x.shape, 'note_x.shape')
print(length_x.shape, 'length_x.shape')
print(note_y.shape, 'note_y.shape')
print(length_y.shape, 'length_y.shape')


logger('TRAINING')

model = create_model(
    categorized_variables=categorized_variables,
    lstm_size=lstm_size,
    lr=lr,
    n_time_steps=n_time_steps,
)

model.summary()
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
          batch_size=batch_size,
          epochs=epochs,
          # callbacks=[play_callback]
          )

save_model(model, 'model')
