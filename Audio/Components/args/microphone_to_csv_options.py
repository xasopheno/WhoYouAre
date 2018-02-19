import os
import sys
import argparse
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))


def microphone_to_csv_options():
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

    a.add_argument("--play_midi",
                   help="Specify if midi should be sent with python-rt-midi).",
                   dest="play_midi",
                   required=False,
                   default=False,
                   type=bool,
                   nargs=1)

    a.add_argument("--play_websocket",
                   help="Specify if frequencies should be sent to websocket).",
                   dest="play_websocket",
                   required=False,
                   default=False,
                   type=bool,
                   nargs=1)

    a.add_argument("--filtered",
                   help="filtered to show only notes).",
                   dest="filtered",
                   required=False,
                   default=False,
                   type=bool,
                   nargs=1)

    a.add_argument("--wave",
                   help="Specify if frequencies should be sent to the python oscillator).",
                   dest="wave",
                   required=False,
                   default=False,
                   type=bool,
                   nargs=1)

    return a.parse_args()
