import os.path
import sys
import re

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
from midi_to_note_number import midi_to_note_number

last_note = 60

def get_data_dir():
    data_dir = os.getcwd() + '/Audio/Data/language'
    return data_dir


def absolute_file_paths(directory):
    for dirpath, _, filenames in os.walk(directory):
        for f in filenames:
            yield os.path.abspath(os.path.join(dirpath, f))


def get_file_name(file):
    regex = '\/WhoYouAre\/Audio\/Data\/language(.*)'
    match_object = re.search(regex, file, flags=0)
    file_name = match_object[1]
    return file_name


def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


def get_file_names():
    data_dir = get_data_dir()
    file_names = []
    for file in absolute_file_paths(data_dir):
        file_name = get_file_name(file)
        if file_name.endswith('.csv'):
            file_names.append(file_name)

    return file_names


def make_columns(line):
    global last_note
    line = list(map(lambda col: col.rstrip('\n,'), line.split(' ')))
    midi_num = (int(line[0]))

    if midi_num == 0:
        line.insert(1, '0')
    else:
        line.insert(1, str(midi_to_note_number[midi_num] + 1))

    interval = midi_num - last_note
    while abs(interval) > 24:
        interval = interval / 2
    if midi_num is not 0 and last_note is not 0:
        line.insert(2, str(interval))
        last_note = midi_num
    else:
        line.insert(2, '0')

    return ' '.join(line)



def concat_csv_files(array_chosen_files):
    data_dir = get_data_dir()
    with open(os.getcwd() + '/Audio/Data/concatenated_csv.csv', 'w') as final:
        for file in absolute_file_paths(data_dir):
            if get_file_name(file) in array_chosen_files:
                with open(file) as content:
                    next(content)
                    for line in content:
                        line = make_columns(line)
                        final.write(line + '\n')
                    print(get_file_name(file))

    print('File Length:', file_len(os.getcwd() + '/Audio/Data/concatenated_csv.csv'))


concat_csv_files(get_file_names()[0])
