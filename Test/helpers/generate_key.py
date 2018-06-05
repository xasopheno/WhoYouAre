from typing import List


def generate_key(root: int, scale: List[int], n_octaves: int) -> List[int]:
    current = root
    midi_key = [root]

    for octave in range(n_octaves):
        for value in scale:
            current += value
            midi_key.append(current)

    print(midi_key)
    return midi_key
