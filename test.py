import unittest
import wave

from gtar import freq


class TestFreq(unittest.TestCase):
    def setUp(self):
        self.wavefile_10k = wave.open('./tests/10kHz.wav', 'rb')
        self.wavefile_1k = wave.open('./tests/1kHz.wav', 'rb')
        self.wavefile_440 = wave.open('./tests/440Hz.wav', 'rb')

    def runTest(self):
        self.assertEqual(int(freq(self.wavefile_10k.readframes(1024))), 10000)
        self.assertEqual(int(freq(self.wavefile_1k.readframes(1024))), 1000)
        self.assertEqual(int(freq(self.wavefile_440.readframes(1024))), 440)


if __name__ == '__main__':
    unittest.main()
