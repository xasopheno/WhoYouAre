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

    return a.parse_args()
