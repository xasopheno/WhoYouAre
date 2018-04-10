from keras.models import model_from_json


def load_model():
    json_file = open('NN/trained_models/27000.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    loaded_model.load_weights("NN/trained_models/27000.h5")
    print("Loaded model from disk")
    return loaded_model
