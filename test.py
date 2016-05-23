import unittest
import wave

from gtar import freq

class TestFreq(unittest.TestCase):
    def setUp(self):
        self.wavefile_10k = wave.open('./test/10kHz_44100Hz_16bit_05s', 'rb')
        self.wavefile_1k = wave.open('./test/1kHz_44100Hz_16bit_05s', 'rb')
        self.wavefile_440 = wave.open('./test/440Hz_44100Hz_16bit_05s', 'rb')

    def runTest(self):
        self.assertEqual(freq(self.wavefile_10k.readframes(1024)), 10000)
        self.assertEqual(freq(self.wavefile_1k.readframes(1024)), 1000)
        self.assertEqual(freq(self.wavefile_440.readframes(1024)), 400)

if __name__ == '__main__':
    TestFreq()
