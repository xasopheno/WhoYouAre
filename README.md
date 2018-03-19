# WhoYouAre

## Setup 
pip3 install requirements.txt

## Use
Generate a .csv file:

`python3 Record.py --display_predictions=True --filtered=True --csv=True`

Copy .csv values from `Audio/data/output_new.csv` to `Audio/data/input.csv`.

Train on the .csv file:

Best to open `WhoYouAre.ipynb` with `jupyter notebook` and train from there,
but network can also be trained with `python3 WhoYouAre.py`

You can then improvise with the trained model with 

`python3 Record.py --nn=True --display_predictions=True --filtered=True`


## Record.py
python3 Record.py

Records microphone input as midi values

#### Arguments
default marked in (parentheses)
* --nn=True | (False)
* --show_prediction=True | (False) 
* --show_volume=True | (False)
* --write_csv=True | (False)
* --play_midi=True | (False)
* --play_websocket=True | (False)
* --filtered=True | (False)
* --py_osc=True | (False)
* --nn=True | (False)

##### nn 
Improvised with a trained model. 

##### show_prediction
Display the predicted midi values, length and volume

##### show_volume
Display the volume visualizer in terminal

##### write_csv
Write the predicted values to a csv file

##### play_midi
Play midi device attached through usb with rt-midi

##### filtered
Filter out repeated notes from stream. Currently this is default and cannot be changed

##### py_osc 
Play local python oscillator (Depricated)

##### play_websockets
Play local websockets server. For use with browser oscillator. (Depricated)


