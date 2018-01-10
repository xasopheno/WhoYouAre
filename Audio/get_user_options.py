import os
import sys
import argparse
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))


def get_user_options():
    a = argparse.ArgumentParser()
    a.add_argument("--volume",
                   help = "Specify if input volume should be displayed.",
                   dest = "display_volume",
                   required=False,
                   default=False,
                   type=bool,
                   nargs=1)

    a.add_argument("--values",
                   help="Specify if prediction values should be displayed).",
                   dest = "display_prediction",
                   required=False,
                   default=False,
                   type=bool,
                   nargs=1)

    a.add_argument("--csv",
                   help="Specify if a csv should be written).",
                   dest="write_csv",
                   required=False,
                   default=False,
                   type=str,
                   nargs=1)

    a.add_argument("--play",
                   help="Specify if midi should be sent with python-rt-midi).",
                   dest="play",
                   required=False,
                   default=False,
                   type=bool,
                   nargs=1)

    return a.parse_args()
