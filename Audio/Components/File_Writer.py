import os


class File_Writer:
    def __init__(self, filename='', write=False):
        self.default_filename = 'output_new.csv'
        self.file_name = self.get_path(filename)
        self.file = open(self.file_name, "w")

        if write:
            self.prepare_file()

    def get_path(self, filename):
        current_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'data'))
        if filename == '':
            filename = self.default_filename

        path = '{0}/{1}'.format(current_path, filename)

        print('Data will be written to:', path)
        return path

    def prepare_file(self):
        self.file.write('note, length, volume\n')

    def write_to_csv(self, predicted_values):
        note = predicted_values['note']
        length = predicted_values['length']
        volume = predicted_values['volume']

        result = '{}, {}, {}\n'.format(note, length, volume)
        self.file.write(result)
