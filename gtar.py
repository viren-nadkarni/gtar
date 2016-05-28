#!/usr/bin/env python

import pyaudio
import numpy
import wave
import time
import sys
from pprint import pprint


tunings = {
        'standard': [
            ('E', 329.63),
            ('B', 246.94),
            ('G', 196.00),
            ('D', 146.83),
            ('A', 110.00),
            ('E', 82.41)
        ]
}

AUDIO_CHANNELS = 1
AUDIO_SAMP_FREQ = 48000
AUDIO_FRAMES_PER_BUFFER = 1024
AUDIO_SAMP_DELAY = 0.5


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
            channels=AUDIO_CHANNELS,
            rate=AUDIO_SAMP_FREQ,
            input=True, 
            frames_per_buffer=AUDIO_FRAMES_PER_BUFFER)

    pprint(tunings['standard'])
    print
    while(True):
        buff = stream.read(AUDIO_FRAMES_PER_BUFFER)
        sys.stdout.write( '\r' + str(freq(buff, AUDIO_SAMP_FREQ, AUDIO_FRAMES_PER_BUFFER)) )
        sys.stdout.flush()
        time.sleep(AUDIO_SAMP_DELAY)

    stream.stop_stream()
    stream.close()
    audio.terminate()


if __name__ == '__main__':
    main()

