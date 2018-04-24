import random


def play_generated_phrase(generated_notes, generated_lengths, player, client=False):
    for event in range(len(generated_notes)):
        note = generated_notes[event]
        length = generated_lengths[event]
        if note > 90 or note < 30: 
          note = 0

        length *= random.choice([1])
        print(note, '|', length)
        if client:
            client.model_output({
                "note": note,
                "length": length,
            })
        player.play(note, length, 100)
