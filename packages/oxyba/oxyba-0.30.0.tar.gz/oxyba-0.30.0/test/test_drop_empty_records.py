import unittest
import numpy.testing as npt
import numpy as np
import oxyba as ox

# nanrow_all


class Test_nanrow_all(unittest.TestCase):
    def test1(self):
        x = np.array([[1, 2, 3], [np.nan, np.inf, np.nan]])
        y = np.array([[1, 2, 3]])
        npt.assert_array_equal(ox.drop_empty_records(x), y)

    def test2(self):
        x = np.array([[1, 2, 3], [np.nan, np.inf, np.nan]])
        y = np.array([1, 2, 3])
        with npt.assert_raises(AssertionError):
            npt.assert_array_equal(
                ox.drop_empty_records(x), y,
                "test is expected to fail bcoz array shapes don't match.")

    def test3(self):
        x = np.array([[1, 2, 3], [4, 5, 6], [np.nan, np.inf, np.nan], [
                     7, 8, 9], [np.inf, np.inf, -np.inf]])
        y = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        npt.assert_array_equal(ox.drop_empty_records(x), y)

    def test4(self):
        x = np.array([[1, 2, 3], [np.nan, np.inf, np.nan]]).T
        y = np.array([[1, 2, 3]]).T
        npt.assert_array_equal(ox.drop_empty_records(x, 0), y)

    def test5(self):
        x = np.array([[1, 2, 3], [np.nan, np.inf, np.nan]]).T
        y = np.array([1, 2, 3]).T
        with npt.assert_raises(AssertionError):
            npt.assert_array_equal(
                ox.drop_empty_records(x, 0), y,
                "test is expected to fail bcoz array shapes don't match.")

    def test6(self):
        x = np.array([[1, 2, 3], [4, 5, 6], [np.nan, np.inf, np.nan], [
                     7, 8, 9], [np.inf, np.inf, -np.inf]]).T
        y = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]]).T
        npt.assert_array_equal(ox.drop_empty_records(x, 0), y)


# run
if __name__ == '__main__':
    unittest.main()
