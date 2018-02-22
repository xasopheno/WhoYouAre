from Audio.Components.helpers.sample import sample


def decode_prediction(encoded_prediction, lookup_index, diversity):
    encoded_index_from_sample = sample(encoded_prediction, diversity)
    decoded_prediction = lookup_index[encoded_index_from_sample]
    return decoded_prediction


def decode_predictions(encoded_prediction, lookup_indicies, diversity):
    encoded_note_prediction = encoded_prediction[0][0]
    encoded_length_prediction = encoded_prediction[1][0]

    note_prediction = decode_prediction(
        encoded_prediction=encoded_note_prediction,
        lookup_index=lookup_indicies['index_note'],
        diversity=diversity
    )

    length_prediction = decode_prediction(
        encoded_prediction=encoded_length_prediction,
        lookup_index=lookup_indicies['index_lengths'],
        diversity=diversity
    )

    predictions = {
        'note_prediction': note_prediction,
        'length_prediction': length_prediction,
    }

    return predictions
