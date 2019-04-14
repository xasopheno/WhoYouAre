from keras.layers import Activation, Input, LSTM, Dense, Dropout, BatchNormalization, GRU, Flatten, TimeDistributed
from keras.models import Model
from keras.layers.merge import concatenate
from keras import optimizers
import constants


def create_model(categorized_variables, lstm_size, lr, n_time_steps, dropout):
    note_input = Input(name='note_input', shape=(n_time_steps, len(categorized_variables['note_categories'])))
    interval_input = Input(name='interval_input', shape=(n_time_steps, len(categorized_variables['interval_categories'])))
    note_name_input = Input(name='note_name_input', shape=(n_time_steps, len(categorized_variables['note_name_categories'])))
    length_input = Input(name='length_input', shape=(n_time_steps, len(categorized_variables['length_categories'])))

    concat = concatenate([note_input, note_name_input, length_input])

    note_branch1 = LSTM(lstm_size, return_sequences=True)(concat)
    length_branch1 = LSTM(lstm_size, return_sequences=True)(length_input)

    #note_branch = LSTM(lstm_size, return_sequences=True)(note_branch)
    #length_branch = LSTM(lstm_size, return_sequences=True)(length_branch)

    #note_branch = LSTM(lstm_size, return_sequences=True)(note_branch)
    #length_branch = LSTM(lstm_size, return_sequences=True)(length_branch)

    #note_branch = LSTM(lstm_size, return_sequences=True)(note_branch)
    #length_branch = LSTM(lstm_size, return_sequences=True)(length_branch)

    #note_branch = LSTM(lstm_size, return_sequences=True)(note_branch)
    #length_branch = LSTM(lstm_size, return_sequences=True)(length_branch)

    #note_branch = LSTM(lstm_size, return_sequences=True)(note_branch)
    #length_branch = LSTM(lstm_size, return_sequences=True)(length_branch)
    
    note_branch2 = LSTM(lstm_size, return_sequences=False)(note_branch1)
    length_branch2 = LSTM(lstm_size, return_sequences=False)(length_branch1)

    output_notes = Dense(len(categorized_variables['note_categories']), activation='softmax', name='note_output')(note_branch2)
    length_output = Dense(len(categorized_variables['length_categories']), activation='softmax', name='length_output')(length_branch2)

    optimizer = optimizers.RMSprop(lr=lr, decay=0.0001)
    model = Model(inputs=[note_input, note_name_input, interval_input, length_input],
                  outputs=[output_notes, length_output])
    model.compile(loss=['categorical_crossentropy', 'categorical_crossentropy'], loss_weights=[1, 0.5], optimizer=optimizer)
    return model
