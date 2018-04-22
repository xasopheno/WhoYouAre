from keras.models import model_from_json
from keras.utils import plot_model


def load_model(model_name):
    json_file_name = 'NN/trained_models/{}.json'.format(model_name)
    json_file = open(json_file_name, 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    model_weights = "NN/trained_models/{}.h5".format(model_name)
    loaded_model.load_weights(model_weights)
    print("Loaded {} from disk".format(model_name))
    return loaded_model


if __name__ == "__main__":
    model = load_model('32000')
    plot_model(model, to_file='model.png')
    # model.summary()

