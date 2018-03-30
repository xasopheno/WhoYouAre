import os.path
import sys
import re

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))


def get_data_dir():
    data_dir = os.getcwd() + '/Audio/Data/language/motifs'
    return data_dir


def absolute_file_paths(directory):
    for dirpath,_,filenames in os.walk(directory):
        for f in filenames:
            yield os.path.abspath(os.path.join(dirpath, f))


def get_file_name(file):
    regex = '\/WhoYouAre\/Audio\/Data\/language(.*)'
    match_object = re.search(regex, file, flags=0)
    file_name = match_object[1]
    return file_name


# def file_len(fname):
#     with open(fname) as f:
#         for i, l in enumerate(f):
#             pass
#     return i + 1

def get_file_names():
    data_dir = get_data_dir()
    file_names = []
    for file in absolute_file_paths(data_dir):
        file_name = get_file_name(file)
        if file_name.endswith('.csv'):
            file_names.append(file_name)

    return file_names


def concat_csv_files(array_chosen_files):
    data_dir = get_data_dir()
    with open(os.getcwd() + '/Audio/Data/concatenated_csv.csv', 'w') as final:
        for file in absolute_file_paths(data_dir):
            if get_file_name(file) in array_chosen_files:
                with open(file) as content:
                    next(content)
                    for line in content:
                        final.write(line)
                    print(get_file_name(file))
        # print('file is ' + len(final) + 'long')


concat_csv_files(get_file_names())
