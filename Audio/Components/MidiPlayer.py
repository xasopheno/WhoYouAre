import time
import rtmidi
import os.path
current_path = os.getcwd()
import csv


class MidiPlayer:
    def __init__(self, synth='Volca'):
        self.synth = synth
        self.midi_out = self.setupMidi()

    def setupMidi(self):
        midi_out = rtmidi.MidiOut()
        # available_ports = midiout.get_ports()
        midi_out.open_port(0)
        return midi_out

    def play(self, num, length, velocity=100):
        if num == 0:
            time.sleep(length)
        else:
            if self.synth == 'Volca':
                self.play_volca(num, length, velocity)
            else:
                self.play_synth(num, length, velocity)

    def play_synth(self, num, length, velocity=100):
        note_on = [0x90, num, velocity]
        note_off = [0x80, num, 0]
        self.midi_out.send_message(note_on)
        time.sleep(length)
        self.midi_out.send_message(note_off)

    def play_volca(self, num, length, velocity=100):
        velocity = [0xb0, 0x29, velocity]
        note_on = [0x90, num, 1]
        note_off = [0x80, num, 0]
        self.midi_out.send_message(velocity)
        self.midi_out.send_message(note_on)
        time.sleep(length)
        self.midi_out.send_message(note_off)

    def del_midiout(self):
        del self.midi_out

    def play_csv(self):
        with open('Audio/data/output.csv', 'r') as f:
            reader = csv.reader(f, delimiter=',')
            next(reader)
            for row in reader:
                note = int(row[0])
                volume = int(row[1])
                length = int(row[2])
                print(note, volume, length)

                try:
                    self.play(note, .03, volume)
                except:
                    print('value was unplayable', note, length, volume)


if __name__ == '__main__':
    player = MidiPlayer()
    player.play_csv()
