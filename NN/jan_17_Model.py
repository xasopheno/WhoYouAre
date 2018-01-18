from keras.layers import Dense, Dropout, BatchNormalization
from keras.layers.recurrent import LSTM
import keras.backend as K


class SimpleModel:
    def __init__(self, visible, lstm_size):
        self.visible = visible
        self.lstm_size = lstm_size

        self.params = {'num': 0}
        setattr(K, 'params', self.params)

    def model(self):
        hidden1 = LSTM(self.lstm_size, return_sequences=True)(self.visible)
        batchNorm1 = BatchNormalization()(hidden1)
        dropout1 = Dropout(0.5)(batchNorm1)

        hidden2 = LSTM(self.lstm_size, return_sequences=True)(dropout1)
        batchNorm2 = BatchNormalization()(hidden2)
        dropout2 = Dropout(0.5)(batchNorm2)

        hidden3 = LSTM(self.lstm_size, return_sequences=True)(dropout2)
        batchNorm3 = BatchNormalization()(hidden3)
        dropout3 = Dropout(0.5)(batchNorm3)
        #
        hidden4 = LSTM(self.lstm_size, return_sequences=True)(dropout3)
        batchNorm4 = BatchNormalization()(hidden4)
        dropout4 = Dropout(0.5)(batchNorm4)

        hidden5 = LSTM(self.lstm_size, return_sequences=True)(dropout4)
        batchNorm5 = BatchNormalization()(hidden5)
        dropout5 = Dropout(0.5)(batchNorm5)

        hidden6 = LSTM(self.lstm_size, return_sequences=True)(dropout5)
        batchNorm6 = BatchNormalization()(hidden6)
        dropout6 = Dropout(0.5)(batchNorm6)

        # hidden7 = LSTM(self.lstm_size, return_sequences=True)(dropout6)
        # batchNorm7 = BatchNormalization()(hidden7)
        # dropout7 = Dropout(0.5)(batchNorm7)
        #
        # hidden8 = LSTM(self.lstm_size, return_sequences=True)(dropout7)
        # batchNorm8 = BatchNormalization()(hidden8)
        # dropout8 = Dropout(0.5)(batchNorm8)

        output = LSTM(self.lstm_size)(dropout6)

        return output
