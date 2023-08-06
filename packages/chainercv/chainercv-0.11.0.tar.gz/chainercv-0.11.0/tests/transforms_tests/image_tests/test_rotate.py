import random
import unittest

import numpy as np

from chainer import testing
from chainercv.transforms import flip
from chainercv.transforms import rotate

try:
    import scipy  # NOQA
    _available = True
except ImportError:
    _available = False


@unittest.skipUnless(_available, 'SciPy is not installed')
class TestRotate(unittest.TestCase):

    def test_rotate(self):
        img = np.random.uniform(size=(3, 32, 24))
        angle = random.uniform(-180, 180)

        out = rotate(img, angle)
        expected = flip(img, x_flip=True)
        expected = rotate(expected, -1 * angle)
        expected = flip(expected, x_flip=True)

        np.testing.assert_almost_equal(out, expected, decimal=6)


testing.run_module(__name__, __file__)
