import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
from Audio.Components.args.csv_player_options import player_options
from Audio.Components.CSVPlayer import CSVPlayer

args = player_options()
print('args: ', args)

if __name__ == '__main__':
    args = player_options()
    print('args: ', args)

    csv_player = CSVPlayer(args=args)
    csv_player.play_csv()
