import unittest
# import numpy.testing as npt
# import numpy as np
import oxyba as ox


# test cases
class Test_german_number(unittest.TestCase):
    def test1(self):
        self.assertEqual(ox.clean_german_number('1.234'), '1234')

    def test2(self):
        self.assertEqual(ox.clean_german_number('1234'), '1234')

    def test3(self):
        self.assertEqual(ox.clean_german_number('+1234'), '1234')

    def test4(self):
        self.assertEqual(ox.clean_german_number('-1234'), '-1234')

    def test5(self):
        self.assertEqual(ox.clean_german_number('1,2'), '1.2')

    def test6(self):
        self.assertEqual(ox.clean_german_number('1,'), '1.')

    def test7(self):
        self.assertEqual(ox.clean_german_number(',2'), '.2')

    def test8(self):
        self.assertEqual(ox.clean_german_number('1.234,56'), '1234.56')

    def test9(self):
        self.assertEqual(ox.clean_german_number('1.234.560'), '1234560')

    def test10(self):
        self.assertEqual(ox.clean_german_number('1.234.560,89'), '1234560.89')

    def test11(self):
        self.assertEqual(ox.clean_german_number('1a2b3c.4d,5e'), '1234.5')

    def test12(self):
        self.assertEqual(ox.clean_german_number(' 1 2 3 4, 5 '), '1234.5')

    def test13(self):
        self.assertEqual(ox.clean_german_number(' 1 23 - 4 , 5+'), '1234.5')

    def test14(self):
        self.assertEqual(ox.clean_german_number('1234.56'), '123456')

    def test21(self):
        self.assertEqual(ox.clean_german_number('123,456.78'), None)

    def test22(self):
        self.assertEqual(ox.clean_german_number('-'), None)

    def test23(self):
        self.assertEqual(ox.clean_german_number('a -'), None)

    def test24(self):
        self.assertEqual(ox.clean_german_number(' - '), None)

    def test25(self):
        self.assertEqual(ox.clean_german_number(' - ,'), None)

    def test26(self):
        self.assertEqual(ox.clean_german_number(','), None)

    def test27(self):
        self.assertEqual(ox.clean_german_number('+'), None)

    def test28(self):
        self.assertEqual(ox.clean_german_number(" a b "), None)

    def test29(self):
        self.assertEqual(ox.clean_german_number("  "), None)

    def test30(self):
        self.assertEqual(ox.clean_german_number("1,2,3"), None)

    def test31(self):
        self.assertEqual(ox.clean_german_number("1.2,3.4"), None)


"""
    def test32(self):
        self.assertEqual( ox.clean_german_number(), )

    def test3(self):
        self.assertEqual( ox.clean_german_number(), )

    def test3(self):
        self.assertEqual( ox.clean_german_number(), )

    def test3(self):
        self.assertEqual( ox.clean_german_number(), )
"""

# run
if __name__ == '__main__':
    unittest.main()
