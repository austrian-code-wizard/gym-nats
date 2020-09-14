import numpy as np
from unittest import TestCase
from gym_nats.utils import numpy_encode, numpy_decode

class Test(TestCase):
    def test_encode(self):
        data = np.array([1, 3, -1000, 3.211]).astype(np.float64)
        encoded = numpy_encode(data)
        self.assertEqual(encoded, b'AAAAAAAA8D8AAAAAAAAIQAAAAAAAQI/A46WbxCCwCUA=')

        data = np.array([1, 3, -1000, 3.211]).astype(np.float32)
        with self.assertRaises(AssertionError):
            numpy_encode(data)

    def test_decode(self):
        encoded = b'AAAAAAAA8D8AAAAAAAAIQAAAAAAAQI/A46WbxCCwCUA='
        data = numpy_decode(encoded)
        self.assertEqual(data.dtype, np.float64)
        for pair in zip(data, np.array([1, 3, -1000, 3.211]).astype(np.float64)):
            self.assertEqual(pair[0], pair[0])

    def test_encode_decode(self):
        data = np.array([1, 3, -1000, 3.211]).astype(np.float64)
        encoded = numpy_encode(data)
        decoded = numpy_decode(encoded)
        self.assertEqual(data.dtype, decoded.dtype)
        for pair in zip(decoded, data):
            self.assertEqual(pair[0], pair[0])