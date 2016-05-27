#!/usr/bin/env python

import pyaudio
import numpy
import wave
import time
import sys


def freq(frames, sampling_frequency=44100, frames_per_buffer=1024):

    # unpack wave and multiply by the window
    frame_array = numpy.array(wave.struct.unpack("%dh" % (len(frames) / 2), frames)) * numpy.blackman(frames_per_buffer) 
    # calculate fft and maximum
    fftout = abs(numpy.fft.rfft(frame_array)) ** 2
    maximum = fftout[1:].argmax() + 1

    if maximum != len(fftout) - 1:
        y0, y1, y2 = numpy.log(fftout[(maximum - 1):(maximum + 2):])
        x1 = (y2 - y0) * 0.5 / (2 * y1 - y2 - y0)
        result = (maximum + x1) * sampling_frequency / frames_per_buffer
    else:
        result = maximum * sampling_frequency / frames_per_buffer

    return result


def main():
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16,
            channels=1,
            rate=48000, 
            input=True, 
            frames_per_buffer=1024)

    sys.stdout.write('\n')
    while(True):
        buff = stream.read(1024)
        sys.stdout.write( '\r' + str(freq(buff, 48000, 1024)) )
        sys.stdout.flush()
        time.sleep(1)


    stream.stop_stream()
    stream.close()
    audio.terminate()

if __name__ == '__main__':
    main()

