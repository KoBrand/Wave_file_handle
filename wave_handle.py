"""
    Author: Konstantin Brand (@KoBrand)
"""

import pyaudio
import struct
import wave
import numpy as np

"""
stereo files should have dimensions (2xY) or (Yx2) !!!
or should be interlaced with given interlace_channel(array)
"""

# ToDo: make it a classe


def waveread(audio_name, separateChannels = True):
    """
    Reads a audio file and returns a normalized wave array of every channel
    wave_array can have separated left right channels if separateChannels = True

    mono:
    \ xHH \ xHH is one Frame
    Sereo:
    \ xHH\ xHH\ xHH\ xHH is one Frame
       l    r    l    r  the channels ar interlaced

    :param
            audio_name: (string) Path and name of the audio file with format ending
            separateChannels: (bool) if the left and right channel should be separated
    :return:
            wave_array: (array or 2darray) normalized array
            sampling_rate: (int) sampling rate
            left_channel: (array) normalized array
            right_channel: (array) normalized array
            mono_channel:(array) normalized array
    """
    # open wave file read binary
    if (audio_name.split(".")[-1] == "wav") | (audio_name.split(".")[-1] == "WAV"):
        wr = wave.open(audio_name, 'rb')
    else:
        print('wrong file format! only WAVE files are supported')
        return

    sampling_rate = wr.getframerate()
    chunk = wr.getnframes()  # length of auidiofile
    bin_array = wr.readframes(chunk)  # binary wave information
    channel_nr = wr.getnchannels()
    quantization = wr.getsampwidth()

    if channel_nr == 1 and quantization == 1:  # 8 bit mono
        # binary to array with numbers
        data = np.array(struct.unpack('BB' * chunk, bin_array))
        # has values from 0 to 255, which have to be changed to [-1:1]
        wave_array = data-np.mean(data)
        wave_array = wave_array / np.max(abs(wave_array))

        left_channel = None
        right_channel = None
        mono_channel = wave_array
        if separateChannels:
            wave_array = de_interlace_channel(wave_array)

        return wave_array, sampling_rate, left_channel, right_channel, mono_channel

    elif channel_nr == 1 and quantization == 2:  # 16 bit mono
        # binary to array with numbers
        data = np.array(struct.unpack('h' * int((len(bin_array) / 2)), bin_array))
        wave_array = data / np.max(abs(data))

        left_channel = None
        right_channel = None
        mono_channel = wave_array

        if separateChannels:
            wave_array = de_interlace_channel(wave_array)

        return wave_array, sampling_rate, left_channel, right_channel, mono_channel

    elif channel_nr == 2 and quantization == 1:  # 8 bit stereo
        # binary to array with numbers
        data = np.array(struct.unpack('BB' * chunk, bin_array))
        # has values from 0 to 255, which have to be changed to [-1:1]
        wave_array = data - np.mean(data)

        # Define channels and avoid clipping
        left_channel = wave_array[::2] / np.max(abs(wave_array))
        right_channel = wave_array[1::2] / np.max(abs(wave_array))
        mono_channel = left_channel + right_channel
        mono_channel = mono_channel / np.max(abs(mono_channel))
        wave_array = wave_array / np.max(abs(wave_array))
        if separateChannels:
            wave_array = de_interlace_channel(wave_array)

        return wave_array, sampling_rate, left_channel, right_channel, mono_channel

    elif channel_nr == 2 and quantization == 2:  # 16 bit stereo
        # stero handling
        data = np.array(struct.unpack('hh' * chunk, bin_array))

        left_channel = data[::2] / np.max(abs(data))
        right_channel = data[1::2] / np.max(abs(data))
        mono_channel = left_channel + right_channel
        mono_channel = mono_channel / np.max(abs(mono_channel))
        wave_array = data / np.max(abs(data))
        if separateChannels:
            wave_array = de_interlace_channel(wave_array)

        return wave_array, sampling_rate, left_channel, right_channel, mono_channel

    else:
        print("not supported channel number or quantization")

    return


def wave_write(storrage_path_and_name, wave_array, samplingrate, mono=False, quantization_bit=16):
    """
    saves a sound_array in a wave file format. 8 bit and 16 bit are supported
    Args:
        wave_array: (ndarray) with range [-1:1]
        samplingrate: (int) usually 44100
        storrage_path_and_name: (string)
        mono: (bool) for stereo 2 dimensions are expected (2xY)
        quantization_bit: 8, 16 is expected

    Further information:
        WAV format	                Min	        Max	        NumPy dtype
        32-bit floating-point	   -1.0	       +1.0	        float32
        32-bit PCM	            -2147483648	+2147483647	    int32
        16-bit PCM	               -32768	  +32767	    int16
        8-bit PCM	                    0	    255	        uint8   Note that 8-bit PCM is unsigned.

    mono: (two bytes)
    \ xHH \ xHH is one Frame
    Sereo: (each channel has two byts)
    \ xHH\ xHH\ xHH\ xHH is one Frame
       l    r    l    r  the channels ar interlaced
    """

    if mono:
        # if it is stereo convert it to mono
        # make format right
        try:
            if array.shape[1] == 2:
                # Transpose
                array = np.transpose(wave_array)
        except:
            pass

        if wave_array.shape[0] == 2:
            wave_array = interlace_channel(wave_array)

        channel_nr = 1
        byte = 2
        if quantization_bit == 8:
            byte = 1
    else:
        channel_nr = 2
        byte = 2

        # If I acidently want to save a mono file as stereo
        # make sure of correct format
        try:
            if array.shape[1] == 2:
                # Transpose
                wave_array = np.transpose(wave_array)
        except:
            pass

        if wave_array.shape[0] == 2:
            wave_array = np.array((wave_array, wave_array))

        if quantization_bit == 8:
            byte = 1

        # interlace two channels if they are separated
        wave_array = interlace_channel(wave_array)

    # set wave parameters
    wave_output = wave.open(storrage_path_and_name, 'wb')
    wave_output.setparams((channel_nr, byte, samplingrate, 0, 'NONE', 'not compressed'))
    # make sure of no clipping
    wave_array = wave_array/np.max(abs(wave_array))

    # convert to binary
    if quantization_bit == 16:
        # as mentioned obove: it has to have a integer value between -32767 and +32767
        # --> 2**15 and the zero
        wave_array = np.round(32767 * wave_array)
        # convert to binary
        data = wave_array.astype(np.int16)

    if quantization_bit == 8:
        # as mentioned above: it has to have a integer value between 0 and 255
        wave_array = wave_array / np.max(abs(wave_array))
        wave_array += 1
        wave_array = wave_array / np.max(abs(wave_array))
        wave_array = np.round(255 * wave_array)
        # convert to binary
        data = wave_array.astype(np.int8)
    else:
        print("quantization not supported: ", quantization_bit)

    # wirte to wave file
    wave_output.writeframes(data)
    wave_output.close()
    print('wave file has been stored to: ' + storrage_path_and_name)
    return


def sound(audio, samplingRate, mono=False, vol=0.9):
    """ Plays a array in range [-1.0, 1.0]
        *new:
            If audio has left and right channel separated  as 2darray
            it will also play
    Args:
        audio: (ndarray or 2darray / (M) or (2xN)) audio array
        samplingRate: (int) sampling rate
        mono: (bool) mono file (True) or stereo file (False)
            mono:
                0, 0 is one Frame
            Stereo:
                0, 1, 0, 1 is one Frame
                l  r  l  r  the channels are interlaced
        vol: (float) value between 0 : 1
    Returns:
    """
    # TODO: detect if channles are sparated by itself
    # call pyauido
    p = pyaudio.PyAudio()

    # make sure of correct datatype
    audio = audio.astype(np.float32)

    # If audio has left and right channel separated:
    # interlace two channels
    audio = interlace_channel(audio)


    if mono:
        channel_number = 1
    else:
        channel_number = 2

    # for paFloat32 sample values must be in range [-1.0, 1.0]
    audio = np.array(audio)
    audio = audio/np.max(abs(audio))

    # open audio stream and give some information to hardware
    stream = p.open(format=pyaudio.paFloat32,
                    channels=channel_number,
                    rate=samplingRate,
                    output=True)
    # ajust Volume
    audio_leveled = audio*vol

    # convert np.array to binary string
    data = audio_leveled.astype(np.float32).tostring()
    print('play!')
    tic = time.clock()
    # write data to the sound card stream
    stream.write(data)

    # for real time processing use
    # start = 0
    # frame_size = 1024
    # while start <= audio.size:
    #    data = audio[start:frame_size+start]
    #    # do some signal processing here
    #    # write modified data to sound card stream
    #    stream.write(data)
    #    start += frame_size

    # close stream and terminate audio object
    stream.stop_stream()
    toc = time.clock()
    print('Duration of audio stream: ', toc - tic)
    stream.close()
    p.terminate()
    print('done!')
    return


def interlace_channel(array):
    """
    Interlaces two separated channels to one.

    For Pyaudio it es required to interlace a stereo channel
        array[0, :] = [0, 0] left channel
        array[1, :] = [1, 1] right channel
        Stereo:
            0, 1, 0, 1 is one Frame
            l  r  l  r  the channels are interlaced
    :param array: (2darray (2xY)) left and right channel separated
    :return: single_array (ndarray)

    """
    # make format right
    try:
        if array.shape[1] == 2:
            # Transpose
            array = np.transpose(array)
    except:
        pass

    if array.shape[0] == 2:
        stereo_to_single_array = np.empty((array[0].size + array[1].size,), dtype=array.dtype)
        stereo_to_single_array[::2] = array[0]
        stereo_to_single_array[1::2] = array[1]
        return stereo_to_single_array

    return array


def de_interlace_channel(array):
    """
    Separates two channels if they were mixed to one array.

    If you read a Audio file it may only give you a one dimensional array even though it is stereo
        Stereo:
            0, 1, 0, 1 is one Frame
            l  r  l  r  the channels are interlaced
    :param array: (ndarray) left and right channel are interlaced
    :return: channels (2ndarray)
             channels[0, :] = left channel
             channels[1, :] = right channel

    """
    left_channel = array[::2]
    right_channel = array[1::2]
    channels = np.array((left_channel, right_channel))
    return channels

if __name__ == "__main__":
    print("this is just a wave file handle lib")
