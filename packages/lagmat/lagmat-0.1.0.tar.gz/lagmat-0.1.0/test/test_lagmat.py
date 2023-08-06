import unittest
from lagmat import lagmat
import numpy as np
import numpy.testing as npt


class Test_lagmat(unittest.TestCase):

    def test1(self):
        A = np.array([1, 2, 3, 4])
        B = lagmat(A, [1, 2])
        C = np.array([[np.nan, np.nan], [1, np.nan], [2, 1], [3, 2]])
        npt.assert_array_equal(B, C)


# run
if __name__ == '__main__':
    unittest.main()
