# Wave_file_handle in Python
=================================================================

A functions to read, write and play wavefiles in Python 
(like in matlab with sound / waveread / audioread)

* Only supports 16 bit and 8 bit wavefiles

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
audio, sampling_rate, left_channel, right_channel, mono_channel = waveread("path/to/file.wav")
```
* write audio file
```
wave_write(wave_array, samplingrate, storrage_path_and_name)
```
* play audio file
```
sound(audio, samplingRate)
```




Further information
-------------------
Here I give some additional Information on wave files in Pyton.

* difference between mono and stereo
```
mono:
    \ xHH \ xHH is one Frame
    Sereo:
    \ xHH\ xHH\ xHH\ xHH is one Frame
       l    r    l    r  the channels ar interlaced
```
* difference between 8bit and 16 bit
```
WAV format	                Min	        Max	        NumPy dtype
32-bit floating-point	    -1.0	       +1.0	        float32
32-bit PCM	           -2147483648 	+2147483647	    int32
16-bit PCM	              -32768	     +32767	       int16
8-bit PCM	                  0	         255	        uint8   Note that 8-bit PCM is unsigned.
```

TODOS
=====
* todos: change it to a classe
* todo sound: detect if channles are sparated by itself


