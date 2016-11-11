# Wave_file_handle in Pyton
=================================================================
A functions to read, write and play wavefiles in Python 
(like in matlab with sound / waveread / audioread)

* Only supports 16 bit and 8 bit wavefiles!

Requirements
------------

You need:

* python3,
* numpy 
* pyaduio

install it via:
```
sudo apt-get install python3 python3-venv build-essential libblas-dev \
 liblapack-dev gfortran-4.9 libatlas-dev libatlas-base-dev
```
and:
```
sudo pip3 install numpy
sudo pip3 install pyaudio
```

Usage:
-----------------
* initialize
```
from wave_file_hande import *
```
* Read audio file
```
audio, sampling_rate, left_channel, right_channel, mono_channel = read_audio("path/to/file.wav", separateChannels = True)

...
```





Further information
-------------------
Here I give some additional Information on wave files in Pyton.

* difference between mono and stereo
* difference between 8bit and 16 bit


TODOS
=====
* todos

