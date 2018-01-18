from keras.layers import Input
import keras
from keras.layers import Dense, Dropout, BatchNormalization
from keras.layers.recurrent import LSTM
import keras.backend as K


class ConvolutionalRNN:
    def __init__(self, visible, n_steps, n_features, n_divisions):
        self.visible = visible
        self.n_steps = n_steps
        self.n_features = n_features
        self.n_divisions = n_divisions

        self.params = {'num': 0}
        setattr(K, 'params', self.params)

        self.branch_input_size = int(self.n_steps)
        self.branch_output_size = int(self.n_steps/n_divisions/n_divisions)

    def splitter(self, x):
        num = K.params['num']
        print('num',num)
        steps = int(self.n_steps/self.n_divisions)
        start = int(num * steps)
        end = int((num+1) * steps)
        x = x[:,start:end]
        print(start,end)
        return x

    def split_shape(self, input_shape):
        return (input_shape[0], int(input_shape[1]/self.n_divisions), input_shape[2])

    def model(self):
        print(self.visible)
        for i in range(0, self.n_divisions):
            params = {'num': i}
            setattr(K, 'params', params)
            vars()["lambda"+str(i)] = keras.layers.Lambda(self.splitter,
                                                          output_shape=self.split_shape)(self.visible)
            vars()["hidden"+str(i)] = LSTM(self.branch_input_size, return_sequences=True)(vars()["lambda"+str(i)])

            vars()["batchNorm"+str(i)] = BatchNormalization()(vars()["hidden"+str(i)])

            vars()["dropout"+str(i)] = Dropout(0.5)(vars()["batchNorm"+str(i)])

            vars()["output"+str(i)] = LSTM(self.branch_output_size, return_sequences=True)(vars()["dropout"+str(i)])
            print(vars()["output"+str(i)])

        concat = keras.layers.concatenate([vars()["output0"], vars()["output1"], vars()["output2"], vars()["output3"]])

        # tdd = keras.layers.TimeDistributed(Dense(self.branch_input_size))(concat)

        hidden10 = LSTM(128, return_sequences=True)(concat)
        batchNorm10 = BatchNormalization()(hidden10)
        dropout10 = Dropout(0.5)(batchNorm10)

        hidden11 = LSTM(128, return_sequences=True)(dropout10)
        batchNorm11 = BatchNormalization()(hidden11)
        dropout11 = Dropout(0.5)(batchNorm11)

        output = LSTM(128)(dropout11)

        return output
