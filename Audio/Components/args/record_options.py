import os
import sys
import argparse
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))


def record_options():
    a = argparse.ArgumentParser()

    a.add_argument("-vol",
                   action='store_true',
                   help="Specify if input volume should be displayed.",
                   dest="display_volume",
                   required=False,
                   )

    a.add_argument("-val",
                   help="Specify if prediction values should be displayed.",
                   action='store_true',
                   dest = "display_prediction",
                   required=False,
                   )

    a.add_argument("-csv",
                   help="Specify if a csv should be written.",
                   action='store_true',
                   dest="write_csv",
                   required=False,
                   default=False,
                   )

    a.add_argument("-midi",
                   help="Specify if midi should be sent with python-rt-midi.",
                   action='store_true',
                   dest="play_midi",
                   required=False,
                   default=False,
                   )

    a.add_argument("-socket",
                   help="Specify if frequencies should be sent to a local websocket.",
                   action='store_true',
                   dest="play_websocket",
                   required=False,
                   default=False,
                   )

    a.add_argument("-filtered",
                   help="filter out redundant notes).",
                   action='store_true',
                   dest="filtered",
                   required=False,
                   default=False,
                   )

    a.add_argument("-py_osc",
                   help="Specify if frequencies should be sent to the python oscillator.",
                   action='store_true',
                   dest="wave",
                   required=False,
                   default=False,
                   )

    a.add_argument("-nn",
                   help="Improvise with neural network.",
                   action='store_true',
                   dest="nn",
                   required=False,
                   default=False,
                   )

    a.add_argument("-model",
                   help="Improvise with neural network.",
                   dest="model",
                   type = str,
                   required=False,
                   nargs=1
                  )

    return a.parse_args()
