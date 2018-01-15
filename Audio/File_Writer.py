import os


class File_Writer:
    def __init__(self, filename=''):
        self.default_filename = 'output.csv'
        self.file_name = self.get_path(filename)
        self.file = open(self.file_name, "w")

        self.prepare_file()

    def get_path(self, filename):
        current_path = os.path.dirname(os.path.abspath(__file__))
        if filename == '':
            filename = self.default_filename

        path = current_path + '/data/' + filename

        print('Data will be written to:', path)
        return path

    def prepare_file(self):
        self.file.write('note, volume, length\n')

    def write_to_csv(self, predicted_values):
        note = predicted_values['note']
        length = predicted_values['length']
        volume = predicted_values['volume']

        result = '{}, {}\n'.format(note, volume)
        self.file.write(result)
