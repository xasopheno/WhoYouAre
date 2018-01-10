import os


class File_Writer:
    def __init__(self, filename = ''):
        self.file_name = self.get_path(filename)
        self.default_filename = 'output.csv'


    def get_file_name(self, filename):
        current_path = os.getcwd()
        if filename == '':
            filename = self.default_filename

        path = current_path + filename
        print(path)
        return path
