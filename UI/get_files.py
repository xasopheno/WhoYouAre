import os.path
import sys
import re

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))


def absolute_file_paths(directory):
    for dirpath,_,filenames in os.walk(directory):
        for f in filenames:
            yield os.path.abspath(os.path.join(dirpath, f))


def get_file_names():
    data_dir = os.getcwd() + '/Audio/Data/language'
    regex = '\/WhoYouAre\/Audio\/Data\/language(.*)'

    file_names = []

    for file in absolute_file_paths(data_dir):
        match_object = re.search(regex, file, flags=0)
        file_name = match_object[1]
        if file_name.endswith('.csv'):
            file_names.append(file_name)

    return file_names
