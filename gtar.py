#!/usr/bin/env python

import pyaudio
import numpy
import wave
import time
import sys


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

audio_channels = 1
audio_rate = 48000
audio_frames_per_buffer = 1024
audio_sampling_delay = 0.25


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
            channels=audio_channels,
            rate=audio_rate,
            input=True, 
            frames_per_buffer=audio_frames_per_buffer)

    sys.stdout.write('\n')
    while(True):
        buff = stream.read(audio_frames_per_buffer)
        sys.stdout.write( '\r' + str(freq(buff, audio_channels, audio_frames_per_buffer)) )
        sys.stdout.flush()
        time.sleep(audio_sampling_delay)

    stream.stop_stream()
    stream.close()
    audio.terminate()


if __name__ == '__main__':
    main()

