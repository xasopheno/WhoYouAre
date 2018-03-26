import os.path
import sys
import re

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))


def absoluteFilePaths(directory):
    for dirpath,_,filenames in os.walk(directory):
        for f in filenames:
            yield os.path.abspath(os.path.join(dirpath, f))


data_dir = os.getcwd() + '/Audio/Data/language'
data_regex = '\/WhoYouAre\/Audio\/Data\/language(.*)'
file_test = re.compile(data_regex)


for file in absoluteFilePaths(data_dir):
    if file.endswith('.csv'):
        print(file_test.match(file))
