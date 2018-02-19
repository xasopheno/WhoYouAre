import os
import sys
import argparse
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))


def player_options():
    a = argparse.ArgumentParser()

    a.add_argument("--filename",
                   help="File in /data to be played",
                   dest="filename",
                   required=True,
                   default=None,
                   type=str,
                   nargs=1)

    a.add_argument("--play_ws",
                   help="Play with ws_player",
                   dest="play_ws",
                   required=False,
                   default=False,
                   type=bool,
                   nargs=1)

    a.add_argument("--play_pyosc",
                   help="Play with pyosc I made",
                   dest="play_pyosc",
                   required=False,
                   default=False,
                   type=bool,
                   nargs=1)

    return a.parse_args()
