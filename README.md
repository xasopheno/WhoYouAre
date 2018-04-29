# WhoYouAre

## Setup 
`pip3 install requirements.txt`

`cd UI/front-end/ && yarn`

## Use
#### Generate a .csv file for training:

`python3 Record.py -val -csv`

Copy .csv values from `Audio/data/output_new.csv` to `Audio/data/input.csv`.

#### Train on the .csv file:

Open `WhoYouAre.ipynb` with `jupyter notebook`

Copy `model.h5` and `model.json` to `NN/trained_networks`
#### You can then improvise with the trained model with 
From the directory `WhoYouAre` run `./client.sh` and `./server.sh`

`python3 Record.py -nn -model=model -cli -val`

#### `Record.py`
```
  -h, --help    show this help message and exit
  -vol          Specify if input volume should be displayed.
  -val          Specify if prediction values should be displayed.
  -csv          Specify if a csv should be written.
  -midi         Specify if midi should be sent with python-rt-midi.
  -socket       Specify if frequencies should be sent to a local websocket.
  -filtered     filter out redundant notes).
  -py_osc       Specify if frequencies should be sent to the python
                oscillator.
  -nn           Improvise with neural network.
  -model MODEL  specify model to be used with network.
  -cli          set flag if using webclient
  
```
