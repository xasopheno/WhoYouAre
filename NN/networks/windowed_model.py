from keras.layers import Activation, Input, LSTM, Dense, Dropout, BatchNormalization, GRU, Flatten, TimeDistributed, Bidirectional
from keras.models import Model
from keras.layers.merge import concatenate
from keras import optimizers
import constants


def create_model(categorized_variables, lstm_size, lr, n_time_steps, dropout):
    note_input = Input(name='note_input', shape=(n_time_steps, len(categorized_variables['note_categories'])))
    length_input = Input(name='length_input', shape=(n_time_steps, len(categorized_variables['length_categories'])))

    note_branch = Bidirectional(LSTM(lstm_size, return_sequences=True))(note_input)
    length_branch = Bidirectional(LSTM(lstm_size, return_sequences=True))(length_input)

    note_dropout = Dropout(dropout)(note_branch)
    length_dropout = Dropout(dropout)(length_branch)

    note_branch = Bidirectional(LSTM(lstm_size, return_sequences=True))(note_dropout)
    note_share = LSTM(int(lstm_size/4), return_sequences=True)(note_dropout)

    length_branch = Bidirectional(LSTM(lstm_size, return_sequences=True))(length_dropout)
    length_share = LSTM(int(lstm_size/4), return_sequences=True)(length_dropout)

    note_merge = concatenate([note_branch, length_share])
    length_merge = concatenate([length_branch, note_share])

    note_lstm = LSTM(lstm_size, return_sequences=True)(note_merge)
    length_lstm = LSTM(lstm_size, return_sequences=True)(length_merge)

    note_dropout = Dropout(dropout)(note_lstm)
    length_dropout = Dropout(dropout)(length_lstm)

    note_lstm = LSTM(lstm_size, return_sequences=False)(note_dropout)
    length_lstm = LSTM(lstm_size, return_sequences=False)(length_dropout)

    output_notes = Dense(len(categorized_variables['note_categories']), activation='softmax', name='note_output')(note_lstm)
    length_output = Dense(len(categorized_variables['length_categories']), activation='softmax', name='length_output')(length_lstm)

    optimizer = optimizers.RMSprop(lr=lr, decay=0.0001)
    model = Model(inputs=[note_input, length_input], outputs=[output_notes, length_output])
    model.compile(loss=['categorical_crossentropy', 'categorical_crossentropy'], loss_weights=[1, 0.5], optimizer=optimizer)
    return model
