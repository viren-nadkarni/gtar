#!/usr/bin/env python

import pyaudio
import numpy
import wave
import time

def freq(frames):
    frame_array = numpy.array(wave.struct.unpack("%dh" % (len(frames) / 2), frames)) * numpy.blackman(1024) 
    fftout = abs(numpy.fft.rfft(frame_array)) ** 2
    maximum = fftout[1:].argmax() + 1

    if maximum != len(fftout) - 1:
        y0, y1, y2 = numpy.log(fftout[maximum - 1 : maximum + 2 : ])
        x1 = (y2 - y0) * .5 / (2 * y1 - y2 - y0)
        result = (maximum + x1) * 44100 / 1024
        print result
    else:
        result = maximum*44100/1024
        print result

def main():
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16,
            channels=1,
            rate=48000, 
            input=True, 
            frames_per_buffer=1024)



    wf = wave.open('./tests/10kHz_44100Hz_16bit_05s', 'rb')
    print freq(wf.readframes(1024))
    

    '''
    while(True):
        buff = stream.read(1024)
        buff = wf.readframes(2048)
        print freq(buff)
        time.sleep(1)
    '''


    stream.stop_stream()
    stream.close()
    audio.terminate()

if __name__ == '__main__':
    main()

